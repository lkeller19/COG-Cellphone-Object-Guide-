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
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('latin_object.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])


@app.route("/arsu_relief")
def arsu_relief():
    queries = load_queries("SPARQL-queries/arsu-relief-translations.rq", "SPARQL-queries/arsu-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('arsu_relief.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])

@app.route("/gad_relief")
def gad_relief():
    queries = load_queries("SPARQL-queries/gad-relief-translations.rq", "SPARQL-queries/gad-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('gad_relief.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])

@app.route("/julius_terentius")
def julius_terentius():
    queries = load_queries("SPARQL-queries/julius-terentius-translations.rq", "SPARQL-queries/julius-terentius-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('julius_terentius.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])

@app.route("/mithras_relief")
def mithras_relief():
    queries = load_queries("SPARQL-queries/mithras-relief-translations.rq", "SPARQL-queries/mithras-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('mithras_relief.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])

@app.route("/votive_relief")
def votive_relief():
    queries = load_queries("SPARQL-queries/votive-relief-translations.rq", "SPARQL-queries/votive-relief-depicts.rq")
    data = query_wd(queries[0], queries[1])

    info = parse_query_data(data[0], data[1])
    sorted_info = sort_data([info[1], info[2]])

    z_indices = z_index(sorted_info)

    titles = get_titles(sorted_info[1])

    return render_template('votive_relief.html', image=info[0], translations=sorted_info[0], depictions=sorted_info[1], page_titles=titles, trans_z_index=z_indices[0], dep_z_index=z_indices[1])

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

# Sorts into reverse order so that the first bounding box added is the largest
# Allows the smallest bounding box to be on top
def sort_data(parsed_data):
    return_data = []

    return_data = [sorted(parsed_data[0], key=bound_area, reverse=True), sorted(parsed_data[1], key=bound_area, reverse=True)]

    return return_data

# get z index of each bounding box
def z_index(parsed_data):
    for d in parsed_data[1]:
        counter = 0
        for num in d[1]:
            d[1][counter] = float(num) + .1
            counter += 1
        d[1][0] -= 2

    merged_data = parsed_data[0] + parsed_data[1]
    sorted_merged_data = sorted(merged_data, key=bound_area, reverse=True)
    counter1 = 0
    counter2 = 0
    z1 = []
    z2 = []

    for d in parsed_data[0]:
        for l in sorted_merged_data:
            if d[1] == l[1]:
                z1.append(counter2)
            counter2 += 1
        counter1 += 1
        counter2 = 0

    counter1 = 0
    for d in parsed_data[1]:
        for l in sorted_merged_data:
            if d[1] == l[1]:
                z2.append(counter2)
            counter2 += 1
        counter1 += 1
        counter2 = 0
    
    return [z1, z2]

def bound_area(element):
    if len(element) == 3:
        w = element[2][2]
        h = element[2][3]
    else:
        w = element[1][2]
        h = element[1][3]
    return w*h

# validation function to make sure sort_data is working properly
def check_sort(array):
    for element in array:
        print(element)
        print(bound_area(element))
    return