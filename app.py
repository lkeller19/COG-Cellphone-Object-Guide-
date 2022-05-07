from turtle import position
from flask import Flask, render_template
import json
import requests

# import wptools -- doesn't work

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

# r = requests.get(url, params = {'format': 'json', 'query': query})
# data = r.json()
# # https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python

# #ABOVE INFO CAN BE USED FOR QUERY ENTRIES

# r = requests.get(url, params = {'format': 'json', 'query': q2})
# d2 = r.json()



app = Flask(__name__)

@app.route("/")
def index():
    queries = load_queries("SPARQL-queries/latin-inscription-translations.rq", "SPARQL-queries/arsu-relief-translations.rq")
    queries2 = load_queries("SPARQL-queries/gad-relief-translations.rq", "SPARQL-queries/julius-terentius-translations.rq")
    queries3 = load_queries("SPARQL-queries/votive-relief-translations.rq", "SPARQL-queries/mithras-relief-translations.rq")

    data = query_wd(queries[0], queries[1])
    data1 = query_wd(queries2[0], queries2[1])
    data2 = query_wd(queries3[0], queries3[1])
    images = []
    images.append(data[0]["results"]["bindings"][0]["image"]["value"])
    images.append(data[1]["results"]["bindings"][0]["image"]["value"])
    images.append(data1[0]["results"]["bindings"][0]["image"]["value"])
    images.append(data1[1]["results"]["bindings"][0]["image"]["value"])
    images.append(data2[0]["results"]["bindings"][0]["image"]["value"])
    images.append(data2[1]["results"]["bindings"][0]["image"]["value"])
    return render_template('index.html', images=images)

@app.route("/qr_code")
def qr_code():
    return render_template('qr_code.html')
@app.route("/latin_inscription")
def latin_inscription():
    queries = load_queries("SPARQL-queries/latin-inscription-translations.rq", "SPARQL-queries/latin-inscription-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('latin_object.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)
    # image = data["results"]["bindings"][0]["image"]["value"]
    # all_transl = data["results"]["bindings"]
    # translations = []

    # for i in range(len(all_transl)):
    #     temp = []
    #     temp.append(all_transl[i]["inscription"]["value"])
    #     temp.append(all_transl[i]["translation"]["value"])
    #     temp.append(split_pos(all_transl[i]["position"]["value"]))

        
    #     translations.append(temp)
    
    # # print(translations)
    # # print(d2)

    # all_depicts = d2["results"]["bindings"]
    # depictions = []

    # for i in range(len(all_depicts)):
    #     temp = []
    #     temp.append(all_depicts[i]["depiction"]["value"])
    #     temp.append(split_pos(all_depicts[i]["position"]["value"]))
    #     depictions.append(temp)

    # return render_template('latin_object.html', image=image, translations=translations, depictions=depictions)

@app.route("/arsu_relief")
def arsu_relief():
    queries = load_queries("SPARQL-queries/arsu-relief-translations.rq", "SPARQL-queries/arsu-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('arsu_relief.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)

@app.route("/gad_relief")
def gad_relief():
    queries = load_queries("SPARQL-queries/gad-relief-translations.rq", "SPARQL-queries/gad-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('gad_relief.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)

@app.route("/julius_terentius")
def julius_terentius():
    queries = load_queries("SPARQL-queries/julius-terentius-translations.rq", "SPARQL-queries/julius-terentius-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('julius_terentius.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)

@app.route("/mithras_relief")
def mithras_relief():
    queries = load_queries("SPARQL-queries/mithras-relief-translations.rq", "SPARQL-queries/mithras-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('mithras_relief.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)

@app.route("/votive_relief")
def votive_relief():
    queries = load_queries("SPARQL-queries/votive-relief-translations.rq", "SPARQL-queries/votive-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])

    titles = get_titles(info[2])

    return render_template('votive_relief.html', image=info[0], translations=info[1], depictions=info[2], page_titles=titles)

def parse_query_data(data, d2):
    image = data["results"]["bindings"][0]["image"]["value"]
    all_transl = data["results"]["bindings"]
    translations = []

    for i in range(len(all_transl)):
        temp = []
        temp.append(all_transl[i]["inscription"]["value"])
        temp.append(all_transl[i]["translation"]["value"])
        temp.append(split_pos(all_transl[i]["position"]["value"]))

        
        translations.append(temp)
    
    # print(translations)
    # print(d2)

    all_depicts = d2["results"]["bindings"]
    depictions = []

    for i in range(len(all_depicts)):
        temp = []
        temp.append(all_depicts[i]["depiction"]["value"])
        temp.append(split_pos(all_depicts[i]["position"]["value"]))
        depictions.append(temp)

    return [image, translations, depictions]

def load_queries(fname_1, fname_2):
    with open(fname_1, 'r') as file:
        query_1 = file.read()

    with open(fname_2, 'r') as file:
        query_2 = file.read()
    # print(query_1)
    return [query_1, query_2]

def query_wd(query, q2):
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()

    r = requests.get(url, params = {'format': 'json', 'query': q2})
    d2 = r.json()

    return [data, d2]

def split_pos(pos_string):
    pct = []

    temp = pos_string.split(":", maxsplit=1)
    pct = temp[1].split(",")

    pct = list(map(float, pct))
    # print(pct)

    return pct

def get_titles(urls):
    titles = []
    for url in urls:
        r = requests.get(url[0])
        js = json.loads(r.content.decode('utf-8'))
        title = js["entities"][list(js["entities"].keys())[0]]["labels"]["en"]["value"]
        titles.append(title)
    return titles