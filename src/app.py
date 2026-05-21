from flask import Flask, jsonify, request

from config import Config, get_db_collection

app = Flask(__name__)

collection = get_db_collection()


@app.route("/receptor", methods=["POST"])
def receive_data():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON inválido"}), 400

        result = collection.insert_one(data)

        return jsonify({"status": "salvo", "db_id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
