from turtle import position
from flask import Flask, render_template
import json
import requests


# probably best to load these queries in from the SPARQL-queries folder 
# and put them in arrays or something for each page
url = 'https://query.wikidata.org/sparql'
query = '''
SELECT DISTINCT ?item ?itemLabel ?image ?inscription ?translation ?position
WHERE 
{
  ?item wdt:P8583 "34184";
        wdt:P18 ?image;
        p:P1684 ?statement1.
  ?statement1 ps:P1684 ?inscription.
  ?statement1 pq:P2441 ?translation.
  ?statement1 pq:P2677 ?position.
 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''

q2 = '''
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

r = requests.get(url, params = {'format': 'json', 'query': q2})
d2 = r.json()



app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/scratch_object")
def scratch():
    return render_template('scratch_object.html')

@app.route("/qr_code")
def qr_code():
    return render_template('qr_code.html')
@app.route("/object")
def object():
    image = data["results"]["bindings"][0]["image"]["value"]
    all_transl = data["results"]["bindings"]
    translations = []

    for i in range(len(all_transl)):
        temp = []
        temp.append(all_transl[i]["inscription"]["value"])
        temp.append(all_transl[i]["translation"]["value"])
        temp.append(all_transl[i]["position"]["value"])
        translations.append(temp)
    
    # print(translations)
    # print(d2)

    all_depicts = d2["results"]["bindings"]
    depictions = []

    for i in range(len(all_depicts)):
        temp = []
        temp.append(all_depicts[i]["depiction"]["value"])
        temp.append(all_depicts[i]["position"]["value"])
        depictions.append(temp)

    return render_template('latin_object.html', image=image, translations=translations, depictions=depictions)
