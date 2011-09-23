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
    d = datastore.Datastore()
    ext = filename.split('.')[1:]
    path = d.insert(uri) + '.' + '.'.join(ext)
    return flask.url_for('get', path=path)

@app.route('/<path>')
def get(path):
    id = path.split('.')[0]
    d = datastore.Datastore()
    f = d.get(id)

    m = re.match('URI:CHK:(\S+):(\S+):(\d+):(\d+):(\d+)', f['uri'])
    url = 'http://tahoe.vtluug.org/{0}/{1}/{2}/{3}/{4}/{5}'.format(m.group(1),
            m.group(2), m.group(3), m.group(4), m.group(5), path)
    return flask.redirect(url)

if __name__ == "__main__":
    app.run(debug=True)
