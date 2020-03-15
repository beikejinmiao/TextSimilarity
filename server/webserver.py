#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
from flask import Flask, render_template
from flask import request
# from flask import jsonify
from libs.segment import tokenizer
from mode import load_corpus, build_models, _check_model_name

app = Flask(__name__)
api_path_root = "/api/iqa/v1"
models = build_models(*load_corpus(), load=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route(api_path_root + '/query', methods=['POST'])
def near_query():
    req_json = request.json
    question = req_json.get("question")
    resp_json = dict()
    if question:
        que_tokens = tokenizer.cut(question)
        active_model = req_json["model"]
        for name in _check_model_name(active_model):
            _startime = time.time()
            results = models[name].nearest(que_tokens, topn=5, score=True)
            costime = (time.time() - _startime) * 1000
            resp_json[name] = {"top_sim": results, "cost_time": "%.2fms" % costime}
    return json.dumps(resp_json, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    app.run(debug=True)

