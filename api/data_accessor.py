import json
import logging


logging.basicConfig(filename='logs/transactions.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level = logging.DEBUG)
logger = logging.getLogger(__name__)
file_data = 'data.json'

def _get_data():
    with open(file_data) as data_file:
        return json.load(data_file)

def _write_data(data):
    with open(file_data, 'w') as data_file:
        json.dump(data, data_file)

def _get_light(name, data):
    if 'lights' in data:
        light = [(i, light) for i, light in enumerate(data['lights']) if light['name'] == name]
        return light[0] if len(light) > 0 else None

def get_all_lights():
    logger.info('Looking at all lights')
    data = _get_data()
    if 'lights' in data:
        return data['lights']

def get_light(name):
    logger.info('Looking at light [{}]'.format(name))
    data = _get_data()
    light = _get_light(name, data)
    return light[1] if light else None

def add_light(values):
    logger.debug('Attempting to add light with values [{}]'.format(values.__str__()))
    light = {}
    data = _get_data()
    if _get_light(values['name'], data):
        raise Exception(400, 'Light [{}] already exists'.format(values['name']))
    light['name'] = values['name']
    light['on'] = 0
    if 'lights' in data:
        data['lights'].append(light)
    else:
        data['lights'] = [light]
    _write_data(data)
    logger.info('Added light [{}]'.format(light['name']))
    return light

def flip_light(values):
    logger.debug('Attempting to flip light [{}]'.format(values['name']))
    data = _get_data()
    light = _get_light(values['name'], data)
    if not light:
        raise Exception(404, 'Light [{}] not found'.format(values['name']))
    light[1]['on'] = (light[1]['on'] + 1) % 2
    data['lights'][light[0]] = light[1]
    logging.info
    _write_data(data)
    logger.info('Light [{}] now {}'.format(light[1]['name'], 'on' if light[1]['on'] else 'off'))
    return light[1]
    
def delete_light(name):
    logger.debug('Attempting to delete light [{}]'.format(name))
    data = _get_data()
    light = _get_light(name, data)
    if light:
        data['lights'].remove(light[1])
        _write_data(data)
        logger.info('Deleted light [{}]'.format(name))

def get_thermostat():
    logger.info('Looking at thermostat')
    data = _get_data()
    if not 'thermostat' in data:
        raise Exception(404, 'Thermostat not found')
    return data['thermostat']

def update_thermostat(values):
    logger.debug('Attempting to update thermostat with values [{}]'.format(values.__str__()))
    data = _get_data()
    if not 'thermostat' in data:
        data['thermostat'] = {'temperature': 70, 'unit': 'F'}
    if ((not 'temperature' in values or not values['temperature']) and 'unit' in values) and values['unit'] and not values['unit'] == data['thermostat']['unit']:
        data['thermostat']['temperature'] = int(data['thermostat']['temperature']*9/5+32) \
            if values['unit'] == 'F' \
            else int((data['thermostat']['temperature']-32)*5/9)
        data['thermostat']['unit'] = values['unit']
    else:
        if 'temperature' in values and values['temperature']:
            data['thermostat']['temperature'] = int(values['temperature'])
        if 'unit' in values and values['unit']:
            data['thermostat']['unit'] = values['unit']
    _write_data(data)
    logger.info('Updated thermostat with values [Temperature: {}, Unit: {}]'.format(data['thermostat']['temperature'], data['thermostat']['unit']))
    return data['thermostat']
