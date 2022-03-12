import shopify as shopify
import yaml
from flask import Flask, request, url_for, redirect

app = Flask(__name__)

@app.route('/display', methods=['POST','GET'])
def display():
    print(request.form['line'])
    return redirect(url_for('index'))

app.run('0.0.0.0','8080')


