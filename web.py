import datastore
import sys
import re
import flask
import urllib2

import config

app = flask.Flask(__name__)

def get_datastore():
    return datastore.Datastore(config.mongo_host, config.mongo_port)

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    try:
        filecap = flask.request.form['filecap']
        filename = flask.request.form['filename']
    except KeyError:
        filecap = flask.request.args.get('filecap')
        filename = flask.request.args.get('filename')
    if filecap is None or len(filecap) <= 0 or filename is None or len(filename) <= 0:
        flask.abort(400)
    d = get_datastore()
    ext = filename.split('.')[1:]
    path = d.insert({'filecap' : filecap}) + '.' + '.'.join(ext)
    return config.baseurl + flask.url_for('get', path=path)

@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
    try:
        url = flask.request.form['url']
    except KeyError:
        url = flask.request.args.get('url')
    if url is None or len(url) <= 0:
        flask.abort(400)
    d = get_datastore()
    path = d.insert({'url' : url})
    return config.baseurl + flask.url_for('get', path=path)

@app.route('/<path>')
def get(path):
    id = path.split('.')[0]
    d = get_datastore()
    f = d.get(id)
    if not f:
        flask.abort(404)

    if 'filecap' in f:
        filename = path.split('?')[0]
        tahoe_url = '/file/{0}/@@named=/{1}'.format(f['filecap'], filename)
        resp = flask.make_response(tahoe_url, 200)
        resp.headers['X-Accel-Redirect'] = tahoe_url
        return resp
    elif 'url' in f:
        url = f['url']
        return flask.redirect(url)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
