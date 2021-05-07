import json
import time
import logging

from flask import Flask, abort, jsonify, request

import data_accessor

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/light', methods=['GET'])
def get_light(): 
    if 'name' in request.args:
        data = data_accessor.get_light(request.args['name'])
        if not data:
            abort(404, description='Light [{}] not found'.format(request.args['name']))
        else:
            return jsonify(message='Found light [{}]'.format(request.args['name']), light=data)
    data = data_accessor.get_all_lights()
    if not data:
        data = []
    return jsonify(message='Found all lights', lights=data)

@app.route('/light', methods=['POST'])
def flip_light():
    if not 'name' in request.args:
        abort(400, description="No name given for light")
    if 'new' in request.args:
        try:
            light = data_accessor.add_light(request.args)
            return jsonify(message="Light [{}] added".format(request.args['name']), light=light)
        except Exception as e:
            abort(e.args[0], description=e.args[1])
    else:
        try:
            light = data_accessor.flip_light(request.args)
        except Exception as e:
            print(e)
            abort(e.args[0], description=e.args[1])
    return jsonify(message="Light [{}] flipped".format(request.args['name']), light=light)

@app.route('/light', methods=['DELETE'])
def delete_light():
    if not 'name' in request.args:
        abort(400, description="No name given for light")
    data_accessor.delete_light(request.args['name'])
    return jsonify(message="Light [{}] deleted".format(request.args['name']))

@app.route('/thermostat', methods=['GET'])
def get_thermostat():
    try:
        thermostat = data_accessor.get_thermostat()
        return jsonify(message='Found thermostat', thermostat=thermostat)
    except Exception as e:
        abort(e.args[0], description=e.args[1])

@app.route('/thermostat', methods=['POST'])
def update_thermostat():
    if 'unit' in request.args and not request.args['unit'] in ['C', 'F', '']:
        abort(400, description="Unit must be either 'C' or 'F'")
    return jsonify(message='Thermostat updated', thermostat=data_accessor.update_thermostat(request.args))

@app.errorhandler(400)
def bad_request(e):
    logger.error(str(e))
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def resource_not_found(e):
    logger.error(str(e))
    return jsonify(error=str(e)), 404
