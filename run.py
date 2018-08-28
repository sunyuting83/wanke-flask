# coding:utf-8
from flask import Flask, jsonify, render_template

app = Flask(__name__)

from modules import api
app.register_blueprint(api)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=3000)