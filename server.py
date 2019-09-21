import csv
from datetime import datetime, timedelta

from flask import Flask, render_template, jsonify


ROLES = ('Tank', 'Damage', 'Support')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    raw_names = set()
    names = set()
    entries = {}
    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            dt = datetime.fromtimestamp(float(row[0]))
            dt = (dt - timedelta(hours=7))
            dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            name = row[1].split('-')[0]
            s_tank = int(row[2])
            s_damage = int(row[3])
            s_support = int(row[4])
            names.add(name)
            raw_names.add(row[1])
            if s_tank == s_damage == s_support == 0:
                continue
            if dt_str not in entries:
                entries[dt_str] = {}
            if name not in entries[dt_str]:
                entries[dt_str][name] = [s_tank, s_damage, s_support]
        columns = {f'{name} ({role})': [] for name in sorted(names) for role in ROLES}
        for dt, entry in entries.items():
            for name in names:
                if name in entry:
                    columns[f'{name} (Tank)'].append(entry[name][0])
                    columns[f'{name} (Damage)'].append(entry[name][1])
                    columns[f'{name} (Support)'].append(entry[name][2])
                else:
                    columns[f'{name} (Tank)'].append(0)
                    columns[f'{name} (Damage)'].append(0)
                    columns[f'{name} (Support)'].append(0)
        final_columns = [
            ['x', *list(entries.keys())]
        ]
        for title in columns.keys():
            if set(columns[title]) != {0}:
                final_columns.append([title, *columns[title]])
    return jsonify(
        columns=final_columns,
        names=list(raw_names)
    )


if __name__ == '__main__':
    app.run(debug=True)
