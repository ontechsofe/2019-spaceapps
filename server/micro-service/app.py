from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime as dt
from base64 import b64decode
from tqdm import tqdm
from requests import post
from threading import Thread
from json import dumps

app = Flask(__name__)
CORS(app)


def extract_date(line_params) -> dt.date:
    DATE_MILLISECOND = line_params[1].split('.')[0]

    return dt.strptime(DATE_MILLISECOND, '%Y-%m-%d %H:%M:%S')


def reset_changed() -> dict:
    return {
        'latitude': False,
        'longitude': False,
        'altitude': False,
        'internal_temp': False,
        'external_temp': False,
        'external_pressure': False,
        'relative_humidity': False,
        'dew_point': False,
        'horizon_image': False,
        'nadir_image': False,
        'heading': False,
        'pitch': False,
        'yaw': False
    }


def values_changed(changed, what) -> dict:
    for change in what:
        changed[change] = True
    return changed


def parse_data(raw_data, name) -> None:
    print("We parsing now baby!")
    LATITUDE = None
    LONGITUDE = None
    ALTITUDE = None
    INTERNAL_TEMP = None
    EXTERNAL_TEMP = None
    EXTERNAL_PRESSURE = None
    RELATIVE_HUMIDITY = None
    DEW_POINT = None
    HORIZON_IMAGE = None
    NADIR_IMAGE = None
    HEADING = None
    PITCH = None
    YAW = None

    changed = reset_changed()
    data = list()
    line_params = raw_data[0].split(',')
    previous_second = extract_date(line_params).second

    # TODO: Make sure to fill a full object first and then continue

    for line in tqdm(raw_data[:len(raw_data)-1]):
        line_params = line.split(',')
        SOURCE = line_params[0].upper()
        PACKET = line_params[3].upper()
        if [SOURCE, PACKET] in [['GPS01', 'GGA'], ['SWNAV', 'HKP'], ['SWNAV', 'POS0'], ['SW_EM', 'HK'], ['SW_EM', 'EM0'], ['SWCDH', 'EVENT'], ['SWNAV', 'AHR0']]:
            DATE = extract_date(line_params)

            # If we enter a new second
            APPROXIMATED = [x for x, y in changed.items() if not y]
            if DATE.second != previous_second:
                element = {
                    'date_time': DATE.strftime('%Y-%m-%d %H:%M:%S'),
                    'latitude': LATITUDE,
                    'longitude': LONGITUDE,
                    'altitude': ALTITUDE,
                    'internal_temp': INTERNAL_TEMP,
                    'external_temp': EXTERNAL_TEMP,
                    'external_pressure': EXTERNAL_PRESSURE,
                    'relative_humidity': RELATIVE_HUMIDITY,
                    'dew_point': DEW_POINT,
                    'approximated': APPROXIMATED,
                    'horizon_image': HORIZON_IMAGE,
                    'nadir_image': NADIR_IMAGE,
                    'heading': HEADING,
                    'pitch': PITCH,
                    'yaw': YAW
                }
                data.append(element)
            previous_second = DATE.second
            if SOURCE == 'GPS01':
                if PACKET == 'GGA':
                    # TODO: LATITUDE =
                    # TODO: LONGITUDE =
                    # TODO: ALTITUDE = float(line_params[13])
                    pass
            elif SOURCE == 'SWNAV':
                if PACKET == 'POS0':
                    LATITUDE = float(line_params[4])
                    LONGITUDE = float(line_params[5])
                    ALTITUDE = float(line_params[6])
                    changed = values_changed(
                        changed, ['latitude', 'longitude', 'altitude'])
                elif PACKET == 'AHR0':
                    HEADING = float(line_params[7])
                    PITCH = float(line_params[11])
                    YAW = float(line_params[12])
                    changed = values_changed(
                        changed, ['heading', 'pitch', 'yaw'])
            elif SOURCE == 'SW_EM':
                if PACKET == 'HK':
                    INTERNAL_TEMP = float(line_params[11])
                    EXTERNAL_TEMP = float(line_params[12])
                    EXTERNAL_PRESSURE = float(line_params[13])
                    RELATIVE_HUMIDITY = float(line_params[14])
                    if line_params[16] != 'NaN':
                        DEW_POINT = float(line_params[16])
                    changed = values_changed(changed, [
                                             'internal_temp', 'external_temp', 'external_pressure', 'relative_humidity', 'dew_point'])
                elif PACKET == 'EM0':
                    INTERNAL_TEMP = float(line_params[4])
                    EXTERNAL_TEMP = float(line_params[5])
                    EXTERNAL_PRESSURE = float(line_params[7])
                    RELATIVE_HUMIDITY = float(line_params[6])
                    if line_params[8] != 'NaN':
                        DEW_POINT = float(line_params[8])
                    changed = values_changed(changed, [
                                             'internal_temp', 'external_temp', 'external_pressure', 'relative_humidity', 'dew_point'])
            elif SOURCE == 'SWCDH':
                if PACKET == 'EVENT':
                    picture_config = line_params[4]
                    if 'Taking onboard image' in picture_config:
                        directory = picture_config.split('/')
                        NADIR_IMAGE = 'CAM1-NADIR/' + \
                            directory[len(directory)-1]
                        changed = values_changed(changed, ['nadir_image'])
                    elif 'Requesting image from NAVEM' in picture_config:
                        directory = picture_config.split('/')
                        HORIZON_IMAGE = 'CAM2-HOR/' + \
                            directory[len(directory)-1]
                        changed = values_changed(changed, ['horizon_image'])

    print("Text Parse Complete!")

    post(url='http://127.0.0.1:5050/parsedData', data={
        'data': dumps(data[1:]),
        'name': name
    })


@app.route('/parse', methods=['POST'])
def parse():
    print("/parse Endpoint reached")
    if 'data' not in request.json.keys() or 'name' not in request.json.keys():
        return 'USAGE: Please send body params as { "name": string, "data": b64string }', 400
    try:
        raw_data = b64decode(request.json['data']).decode('utf-8').split('\n')
    except:
        return 'Something went wrong decoding the base64 data!', 400
    name = request.json['name']
    thread = Thread(target=parse_data, args=[raw_data, name])
    thread.start()
    return 'Data is being parsed', 200


if __name__ == '__main__':
    app.run(debug=True)
