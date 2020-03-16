#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import json
from flask import Flask, render_template
from flask import request
# from flask import jsonify
from libs.segment import tokenizer
from mode import load_corpus, build_models, _check_model_name
from conf.config import web_host, web_port

app = Flask(__name__)
models = build_models(*load_corpus(), load=True)


def _query_handle(question, modelist, topn=5, score=False):
    resp_json = dict()
    if question and len(modelist) > 0:
        print(question)
        print(modelist)
        que_tokens = tokenizer.cut(question)
        for name in modelist:
            _startime = time.time()
            results = models[name].nearest(que_tokens, topn=topn, score=score)
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
    try:
        req_json = request.json
        topn = int(req_json.get("topn", 0))
        topn = topn if topn > 0 else 5
        return _query_handle(req_json.get("question"),
                             _check_model_name(req_json["model"]),
                             topn=topn)
    except:
        return "There are maybe some errors occurred in execution. Please check your parameters that committed."


@app.route('/iqa/sim/query', methods=['GET'])
def near_get_query():
    try:
        topn = int(request.args.get("topn", 0))
        topn = topn if topn > 0 else 5
        score = request.args.get("score", "false").lower()
        score = True if score == "true" else False
        return _query_handle(request.args.get("question"),
                             _check_model_name(request.args.get("model").split(",")),
                             topn=topn, score=score)
    except:
        return "There are maybe some errors occurred in execution. Please check your parameters that committed."


if __name__ == '__main__':
    app.run(host=web_host, port=web_port, debug=True)

