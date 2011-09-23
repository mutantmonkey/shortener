import datastore
import sys
import re
import flask
import urllib2

import config

app = flask.Flask(__name__)

@app.route('/publish')
def publish():
    try:
        uri = flask.request.form['uri']
        filename = flask.request.form['filename']
    except KeyError:
        uri = flask.request.args.get('uri')
        filename = flask.request.args.get('filename')
    if uri is None or len(uri) <= 0 or filename is None or len(filename) <= 0:
        return 401
    d = datastore.Datastore()
    ext = filename.split('.')[1:]
    path = d.insert({'uri' : uri}) + '.' + '.'.join(ext)
    return flask.url_for('get', path=path)

@app.route('/shorten')
def shorten():
    try:
        url = flask.request.form['url']
    except KeyError:
        url = flask.request.args.get('url')
    if url is None or len(url) <= 0:
        return 401
    d = datastore.Datastore()
    path = d.insert({'url' : url})
    return flask.url_for('get', path=path)

@app.route('/<path>')
def get(path):
    id = path.split('.')[0]
    d = datastore.Datastore()
    f = d.get(id)

    if 'uri' in f:
        filename = path.split('?')[0]
        r = urllib2.urlopen('{0}/file/{1}/@@named=/{2}'.format(
                config.tahoe_backend, f['uri'], filename))
        headers = r.info()
        content = r.read()

        resp = flask.make_response(content, 200)
        resp.headers['Content-Type'] = headers['Content-Type']
        resp.headers['Content-Length'] = headers['Content-Length']
        resp.headers['Etag'] = headers['Etag']
        return resp
    else:
        url = f['url']
        return flask.redirect(url)

if __name__ == "__main__":
    app.run(debug=True)
