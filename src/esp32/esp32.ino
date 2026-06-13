#include <WiFi.h>
#include "time.h"
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 14
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define TEMTPIN 32

TaskHandle_t taskColeta;
TaskHandle_t taskMonWiFi;
SemaphoreHandle_t mutex;

// Mantido apenas os 3 dados dos 2 sensores reais
typedef struct {
  float temperatura;
  float umidade;
  float luminosidade;
} Medidas_t;

Medidas_t med;
DynamicJsonDocument post(1024);
String uid;

String serverName = "http://0.0.0.0:5000/receptor";

// Configs do wifi
char *ssid = "wifi";
char *pwd = "senha";

// Configs do servidor NTP (Ajustado para UTC)
char *ntpServer = "br.pool.ntp.org";
long gmtOffset = 0; 
int daylight = 0;

time_t now;
struct tm timeinfo;
unsigned long ultimoEnvio = 0;

void tColeta(void *pvParameters)
{
  Serial.println("Task de Coleta de Dados Iniciada");
  while(true){
    float t = dht.readTemperature();
    float h = dht.readHumidity();

    int valorLuz = analogRead(TEMTPIN);

    Serial.print("Valor CRU do ADC: ");
    Serial.println(valorLuz);
    
    float porcentagemLuz = (valorLuz / 4095.0) * 100.0;

    xSemaphoreTake(mutex, portMAX_DELAY);
    
    if (isnan(t) || isnan(h)) {
      Serial.println("Falha ao ler o sensor DHT22!");
    } else {
      med.temperatura = t;
      med.umidade = h;
    }
    
    med.luminosidade = porcentagemLuz;
    
    xSemaphoreGive(mutex);
    
    vTaskDelay(pdMS_TO_TICKS(2000)); 
  }
}

void connectWiFi()
{
  Serial.print("Conectando ao WiFI ");
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado com sucesso!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  configTime(gmtOffset, daylight, ntpServer);
}

void tTemInternet(void *pvParameters)
{
  Serial.println("Task Monitor de Internet Iniciada");
  while(true){
    if (WiFi.status() != WL_CONNECTED){
      connectWiFi();
    }
    vTaskDelay(pdMS_TO_TICKS(30000));
  }
}

void sincronizaTempo(void)
{
  if (!getLocalTime(&timeinfo))
  {
    Serial.println("Erro ao acessar o servidor NTP"); 
  }
  else
  {
    Serial.print("Data/Hora Atualizada: ");
    time(&now);
    Serial.println(ctime(&now));
  }
}

void setup() {
  Serial.begin(115200);
  uid = "4022D87364C8";

  dht.begin();

  pinMode(TEMTPIN, INPUT);
  
  mutex = xSemaphoreCreateMutex();
  if (mutex == NULL) Serial.println("Erro ao criar o mutex");

  WiFi.begin(ssid, pwd);

  xTaskCreatePinnedToCore(
    tColeta, "TaskColeta", 4096, NULL, 1, &taskColeta, 0
  );

  xTaskCreatePinnedToCore(
    tTemInternet, "MonitoraWiFi", 4096, NULL, 1, &taskMonWiFi, 1
  );
}

void loop() {
  if ((millis() - ultimoEnvio >= 20000) && (WiFi.status() == WL_CONNECTED))
  {
    ultimoEnvio = millis();
    Serial.println("\n-->> Hora de transmitir dados...");
    
    sincronizaTempo();
    
    xSemaphoreTake(mutex, portMAX_DELAY);
    post.clear();
    post["uid"] = "QUALIDADE_AR-" + uid;
    post["unixtime"] = time(&now);
    post["temperatura"] = med.temperatura;
    post["umidade"] = med.umidade;
    post["luminosidade"] = med.luminosidade;
    xSemaphoreGive(mutex);

    WiFiClient wclient;
    HTTPClient http_post;

    http_post.begin(wclient, serverName);
    http_post.addHeader("Content-Type","application/json");
    http_post.addHeader("x-api-key","soijd7ehdhwdh7a3ihaih");
  
    String tmp;
    serializeJson(post, tmp);
    
    Serial.println("Enviando JSON: " + tmp);
    int http_get_code = http_post.POST(tmp.c_str());

    Serial.print("HTTP CODE = ");
    Serial.println(http_get_code);
    
    if (http_get_code > 0) {
      Serial.println("Resposta do Servidor:");
      Serial.println(http_post.getString());
    } else {
      Serial.print("Erro no POST: ");
      Serial.println(http_post.errorToString(http_get_code).c_str());
    }
    http_post.end();
  }
  
  delay(100);
}