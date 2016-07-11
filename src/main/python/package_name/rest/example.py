from . import *

@app.route('/example', methods=['GET'])
def get_example():
    return flask.jsonify({'test' : 'test'})

@app.route('/example', methods=['PUT'])
def put_example():
    return flask.Response(status=STATUS_CREATED)