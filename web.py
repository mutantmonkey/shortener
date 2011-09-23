import datastore
import sys
import re
import flask
import urllib2

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
        m = re.match('URI:CHK:(\S+):(\S+):(\d+):(\d+):(\d+)', f['uri'])
        url = 'http://tahoe.vtluug.org/{0}/{1}/{2}/{3}/{4}/{5}'.format(
                m.group(1), m.group(2), m.group(3), m.group(4), m.group(5),
                path)
    else:
        url = f['url']
    return flask.redirect(url)

if __name__ == "__main__":
    app.run(debug=True)
