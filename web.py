import datastore
import sys
import re
import flask
import urllib2

import config

app = flask.Flask(__name__)

def get_datastore():
    return datastore.Datastore(config.mongo_host, config.mongo_port)

@app.route('/publish')
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

@app.route('/shorten')
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
        try:
            r = urllib2.urlopen('{0}/file/{1}/@@named=/{2}'.format(
                    config.tahoe_backend, f['filecap'], filename))
            headers = r.info()
            content = r.read()
        except urllib2.HTTPError, e:
            flask.abort(e.code)

        resp = flask.make_response(content, 200)
        resp.headers['Content-Type'] = headers['Content-Type']
        resp.headers['Content-Length'] = headers['Content-Length']
        resp.headers['Etag'] = headers['Etag']
        return resp
    elif 'url' in f:
        url = f['url']
        return flask.redirect(url)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
