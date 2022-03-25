import json

with open('../stationLv3_zh.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

initial_django_data = []
for i, item in enumerate(data):
    row_data = {
        'model': "api.station",
        "fields": {
            "name": item['name'],
            "code": item['code'],
        }
    }
    initial_django_data.append(row_data)

with open('../initial_station_data.json', 'w') as f:
    json.dump(initial_django_data, f)