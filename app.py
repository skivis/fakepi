from time import time
from flask import Flask, request, jsonify


def uniqid():
    return hex(int(time()*10000000))[2:]


app = Flask(__name__)

# Our fake icons "database"
ICONS_DB = [
    {'id': '35dabb9b2373c0', 'name': 'Coca Cola', 'imageUrl': 'https://<s3-bucket-url>/COCA_COLA.png'},
    {'id': '35dabba478c740', 'name': 'Berkshire', 'imageUrl': 'https://<s3-bucket-url>/BERKSHIRE.png'},
    {'id': '35dabbcd9ae452', 'name': 'Atlas Air', 'imageUrl': 'https://<s3-bucket-url>/ATLAS_AIR.png'},
    {'id': '35dabbd337095c', 'name': 'Microsoft', 'imageUrl': 'https://<s3-bucket-url>/MICROSOFT.png'},
    {'id': '35dabbda06fd64', 'name': 'Apple Inc', 'imageUrl': 'https://<s3-bucket-url>/APPLE_INC.png'},
]

@app.route('/_status', methods=['GET'])
def status():
    return jsonify({
        'message': 'Icons service operational.',
        'statusCode': 200
    })


@app.route('/icons', methods=['GET', 'POST'])
def icon_list():
    # POST /icons
    if request.method == "POST":
        data = request.get_json(silent=True)
        try:
            icon = {'name': data['name'], 'imageUrl': data['imageUrl']}
        except KeyError:
            return jsonify({
                'message': 'Failed to save icon, check payload.',
                'statusCode': 400
            }), 400

        # Save to "database" and return resource
        icon['id'] = uniqid()
        ICONS_DB.append(icon)
        return jsonify(icon)

    # GET /icons
    return jsonify({
        'count': len(ICONS_DB),
        'data': ICONS_DB
    })


@app.route('/icons/view/<icon_id>', methods=['GET'])
def icon_detail(icon_id):
    # GET /icons/<icon_id>
    for icon in ICONS_DB:
        if icon['id'] == icon_id:
            return jsonify(icon)
    return not_found()


@app.route('/icons/<icon_id>', methods=['GET', 'PUT', 'DELETE'])
def icon_location(icon_id):
    # PUT /icons/<icon_id>
    if request.method == "PUT":
        data = request.get_json(silent=True)
        for icon in ICONS_DB:
            # only allow updates on existing resources
            if icon['id'] == icon_id:
                icon['name'] = data.get('name', icon['name'])
                icon['imageUrl'] = data.get('imageUrl', icon['imageUrl'])
                return jsonify(icon)

        # If not in "database", respond with 404
        return not_found()

    # DELETE /icons/<icon_id>
    elif request.method == 'DELETE':
        for icon in ICONS_DB:
            if icon['id'] == icon_id:
                ICONS_DB.remove(icon)
                return '', 204
        return not_found()

    # GET /icons/<icon_id>
    response = jsonify()
    response.status_code = 302
    response.headers['location'] = 'https://<s3-bucket-url>/default.png'
    for icon in ICONS_DB:
        if icon['id'] == icon_id:
            response.headers['location'] = icon['imageUrl']
            break
    return response


@app.errorhandler(404)
def not_found(error=None):
    return jsonify(statusCode=404, message='Resource not found'), 404


@app.errorhandler(500)
def internal_server_error(error=None):
    return jsonify(statusCode=500, message='Internal Error, sorry =('), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    return jsonify(statusCode=500, message='Internal Error, sorry =('), 500
