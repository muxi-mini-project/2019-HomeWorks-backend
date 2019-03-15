import requests
from flask import jsonify, request
from . import app

@app.route('/notice/', methods=['GET'])
def notice():
    pass
