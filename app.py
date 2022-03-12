from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/orders_webhook', methods=['POST'])
def display():
    request_data = request.get_json()
    print(request_data)
    status_code = Response(status=201)
    return status_code

app.run('0.0.0.0','8080')


