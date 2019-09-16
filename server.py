import csv
from datetime import datetime

from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    timeseries = set()
    data = {}
    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[1]
            if name not in data:
                data[name] = []
            data[name].append([row[2], row[3], row[4]])
            time = datetime.fromtimestamp(float(row[0])).strftime('%Y-%m-%d %H:%M:%S')
            timeseries.add(time)
    columns = [
        ['x', *timeseries]
    ]
    for name, values in data.items():
        for index, role in enumerate(['Tank', 'Damage', 'Support']):
            display_name = '{} ({})'.format(name.split('-')[0], role)
            values_for_role = [row[index] for row in values]
            columns.append((
                display_name,
                *values_for_role
            ))
    return jsonify(columns=columns)


if __name__ == '__main__':
    app.run(debug=True)
