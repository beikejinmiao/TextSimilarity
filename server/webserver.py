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
models = build_models(*load_corpus(), load=True)


def _query_handle(question, modelist):
    resp_json = dict()
    if question and len(modelist) > 0:
        print(question)
        print(modelist)
        que_tokens = tokenizer.cut(question)
        for name in modelist:
            _startime = time.time()
            results = models[name].nearest(que_tokens, topn=5, score=True)
            costime = (time.time() - _startime) * 1000
            resp_json[name] = {"top_sim": results, "cost_time": "%.2fms" % costime}
    return json.dumps(resp_json, ensure_ascii=False, indent=4)


@app.route('/')
def usage():
    return render_template('usage.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/api/iqa/sim/query', methods=['POST'])
def near_post_query():
    req_json = request.json
    return _query_handle(req_json.get("question"), _check_model_name(req_json["model"]))


@app.route('/iqa/sim/query', methods=['GET'])
def near_get_query():
    print(request.args.get("question"))
    print(request.args.get("model"))
    return _query_handle(request.args.get("question"), _check_model_name(request.args.get("model").split(",")))


if __name__ == '__main__':
    app.run(debug=True)

