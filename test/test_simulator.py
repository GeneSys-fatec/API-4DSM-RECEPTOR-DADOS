import requests

from src.simulator import main


def test_simulator_main_success(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 201

    # Quebramos o loop infinito propositalmente disparando uma KeyboardInterrupt no primeiro sleep!
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)

    main()
    mock_post.assert_called_once()


def test_simulator_main_api_error(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"

    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    main()
    mock_post.assert_called_once()


def test_simulator_main_connection_error(mocker):
    mock_post = mocker.patch(
        "requests.post", side_effect=requests.exceptions.RequestException("Conn Refused")
    )
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    main()
    mock_post.assert_called_once()
