from flask import Flask, request, render_template
from task_five.search import search
import json
import os

CWD = '/'.join([path for path in os.getcwd().split('/') if os.getcwd().split('/').index(path)
                <= os.getcwd().split('/').index('infosearch')])
app = Flask(__name__, template_folder='{}/task_one/output'.format(CWD))


@app.route('/search')
def search_something():
    if 'query' in request.args.keys():
        return json.dumps(list(search(request.args['query']).keys()))
    else:
        return json.dumps({'errors': 'You must enter query parameter'})


@app.route('/<page>')
def get_page(page):
    return render_template(page)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)