from flask import Flask, render_template
import json
import requests

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT DISTINCT ?item ?itemLabel ?image ?depiction ?position
WHERE 
{
  ?item wdt:P8583 "34184";
        wdt:P18 ?image;
        p:P180 ?statement1.
  ?statement1 ps:P180 ?depiction.
  ?statement1 pq:P2677 ?position.
 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''

r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()
# https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python

#ABOVE INFO CAN BE USED FOR QUERY ENTRIES



app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/scratch_object")
def scratch():
    return render_template('scratch_object.html')

@app.route("/object")
def object():
    image = data["results"]["bindings"][0]["image"]["value"]
    return render_template('latin_object.html', image=image)