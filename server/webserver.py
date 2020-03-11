#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify


app = Flask(__name__)
api_path_root = "/api/iqa/v1"


@app.route(api_path_root + '/model/list', methods=['GET'])
def model_list():
    pass

