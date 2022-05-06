import json
import routeros_api
from flask import Flask


def get_connection():
    try:
        connection = routeros_api.RouterOsApiPool(
            '192.168.93.48',
            username='admin',
            password='TT$_M!K',
            plaintext_login=True)
        return connection.get_api()
    except Exception as e:
        print(e)


def get_last_log(rows_amount):
    api = get_connection()
    try:
        list_queues = api.get_resource('/log')
        result = list_queues.get()[-rows_amount:]
        print(result)
        return result
    except Exception as e:
        print(e)


def restart_device():
    api = get_connection()
    try:
        api.get_binary_resource('/').call('restart')
        return 'Restart command sent'
    except Exception as e:
        print(e)
        return 'Device is off'


app = Flask(__name__)


@app.route("/")
def hello():
    return "/get_log/<amount of rows>, /restart"


@app.route('/get_log/<amount_rows>', methods=['GET'])
def get_log(amount_rows):
    amount = int(amount_rows)
    json_result = json.dumps(get_last_log(amount))
    return json_result


@app.route('/restart', methods=['GET'])
def restart():
    return restart_device()


if __name__ == "__main__":
    app.run(debug=True)
