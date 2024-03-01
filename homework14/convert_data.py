import csv
import json
from datetime import datetime

def make_authors_json(csvFilePath, jsonFilePath):
	authors = []
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for rows in csvReader:
			data = {}
			data["fullname"] = rows["fullname"]
			data["born_date"] = rows["born_date"]
			data["born_location"] = rows["born_location"]
			description = rows["description"].strip().removeprefix("\n").removesuffix("\n").strip()
			data["description"] = description
			authors.append(data)
	with open(jsonFilePath, 'w', encoding='utf-8') as json_file:
		json_file.write(json.dumps(authors))

def make_quotes_json(csvFilePath, jsonFilePath):
	quotes = []
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for rows in csvReader:
			data = {}
			data["tags"] = rows["keywords"].split(",")
			data["author"] = rows["author"]
			data["quote"] = rows["quote"]
			quotes.append(data)
	with open(jsonFilePath, 'w', encoding='utf-8') as json_file:
		json_file.write(json.dumps(quotes))