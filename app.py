from flask import Flask, render_template

import requests

# url = 'https://query.wikidata.org/sparql'
# query = '''
# SELECT ?item ?instance_of ?instance_ofLabel WHERE {
#   ?item wdt:P131 wd:Q464266.
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
#   OPTIONAL { ?item wdt:P18 ?instance_of. }
# }
# '''

# r = requests.get(url, params = {'format': 'json', 'query': query})
# data = r.json()
# print(data)

#ABOVE INFO CAN BE USED FOR QUERY ENTRIES



app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/object")
def object():
    return render_template('scratch_object.html')

