#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from flask import Flask, jsonify, request, abort
import random

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

rotation={
  "response" : None,
  "result" : 0,
  "errorCode" : 0,
  "errorMsg" : None,
  "data" : {
    "rotation" : 1
  }
}

baseresponse={
  "response" : None,
  "result" : 0,
  "errorCode" : 0,
  "errorMsg" : None,
}

base_error_response={
  "response" : None,
  "result" : 0,
  "errorCode" : -1,
  "errorMsg" :"I am server error"
}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/rotation', methods=['GET'])
def get_rotation():
    return jsonify(rotation)

@app.route('/clearappdata', methods=['POST'])
def clear_app_data():
    if not request.json:
        abort(400)
    print request.json
    num=random.randint(1,5)
    if num%5==0:
        return jsonify(base_error_response)
    return jsonify(base_error_response)

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify({"message":"server error"})
    response.status_code = 500
    return response

def start():
    app.run(debug=True)

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

start()