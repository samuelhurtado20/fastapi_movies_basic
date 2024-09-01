# db/__init__.py

import json
file = open("db/data.json", encoding="utf-8")
data = json.load(file)

file.close()