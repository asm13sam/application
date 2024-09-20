#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bottle import Bottle, response, request
import json
import sqlite3
import model

REAL_DELETE = 1
SHORT_FORM = 1
WITH_DEACTIVATED = 1
DEACTIVATED_ONLY = 2
ACTIVE_ONLY = 0

app = Bottle()

with open ('model.json', "r") as f:
    app_model = json.loads(f.read())
con_to = sqlite3.connect('base.db')
repo = model.MakeSql(app_model, con_to)

with open ('config.json', "r") as f:
    cfg = json.loads(f.read())

@app.route('/api/<table_name>/<uid:int>')
def get_item(table_name, uid):
    extended = request.query.short != SHORT_FORM
    return repo.get(table_name, uid, extended)
    
@app.route('/api/<table_name>')
def get_list(table_name):
    extended = request.query.short != SHORT_FORM
    get_all = ACTIVE_ONLY
    if request.query.all:
        get_all = request.query.all
    return repo.get_all(table_name, extended, get_all)

@app.post('/api/<table_name>')
def create_measure(table_name):
    data = request.json
    return repo.create(table_name, data)

@app.put('/api/<table_name>/<uid:int>')
def update_measure(table_name, uid):
    data = request.json
    return repo.update(table_name, data, uid)    

@app.delete('/api/<table_name>/<uid:int>/')
def delete(table_name, uid):
    if request.query.delete == REAL_DELETE:
        return repo.delete(table_name, uid)
    return repo.deactivate(table_name, uid)


app.run(debug=True, reloader=True, port=cfg['port'], host="0.0.0.0")
