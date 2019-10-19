from flask import Flask, request
from os import path
from datetime import datetime as dt
from json import dumps, loads
from base64 import b64decode

app = Flask(__name__)

def extract_date(line_params) -> dt.date:
    DATE_MILLISECOND = line_params[1].split('.')[0]
    
    return dt.strptime(DATE_MILLISECOND, '%Y-%m-%d %H:%M:%S')

@app.route('/upload', methods=['POST'])
def upload():
    raw_data = b64decode(request.json['text']).decode('utf-8').split('\n')
    data = list()
    line_params = raw_data[0].split(',')
    previous_second = extract_date(line_params).second

    LATITUDE = None
    LONGITUDE = None
    ALTITUDE = None
    INTERNAL_TEMP = None
    EXTERNAL_TEMP = None
    EXTERNAL_PRESSURE = None
    RELATIVE_HUMIDITY = None
    DEW_POINT = None

    # TODO: Make sure to fill a full object first and then continue

    for line in raw_data[:len(raw_data)-1]:
        line_params = line.split(',')
        SOURCE = line_params[0].upper()
        PACKET = line_params[3].upper()
        if [SOURCE, PACKET] in [['GPS01', 'GGA'], ['SWNAV', 'HKP'], ['SWNAV', 'POS0'], ['SW_EM', 'HK'], ['SW_EM', 'EM0']]:
            DATE = extract_date(line_params)

            # If we enter a new second
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
                    'dew_point': DEW_POINT
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
            elif SOURCE == 'SW_EM':
                if PACKET == 'HK':
                    INTERNAL_TEMP = float(line_params[11])
                    EXTERNAL_TEMP = float(line_params[12])
                    EXTERNAL_PRESSURE = float(line_params[13])
                    RELATIVE_HUMIDITY = float(line_params[14])
                    DEW_POINT = float(line_params[16])
                elif PACKET == 'EM0':
                    INTERNAL_TEMP = float(line_params[4])
                    EXTERNAL_TEMP = float(line_params[5])
                    EXTERNAL_PRESSURE = float(line_params[7])
                    RELATIVE_HUMIDITY = float(line_params[6])
                    DEW_POINT = float(line_params[8])
    print("Text Parse Complete!")
    return dumps(data)

if __name__ == '__main__':
    app.run(debug=True)
    # print(upload())