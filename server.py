import csv
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    names = set()
    timeseries = set()
    data = {}
    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[1]
            names.add(name)
            if name not in data:
                data[name] = []
            data[name].append([row[2], row[3], row[4]])
            time = datetime.fromtimestamp(float(row[0]))
            time = (time - timedelta(hours=7))
            timeseries.add(time.strftime('%Y-%m-%d %H:%M:%S'))
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
    for column in columns[:]:
        if set(column[1:]) == {'0'}:
            columns.remove(column)
    return jsonify(
        columns=columns,
        names=list(names)
    )


if __name__ == '__main__':
    app.run(debug=True)
