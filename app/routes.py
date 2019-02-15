from app import app
import os
from flask import Flask, render_template, json, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "stores.json")
stores = json.load(open(json_url))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get-stores')
def getStoresByName():

    searchString = request.args.get('searchString')

    if searchString:
        results = filter(stores, searchString)
        results.sort(key=getMatchedPostcode, reverse=True)

    return json.dumps([city for (city, matchedPostcode) in results ])

def getMatchedPostcode(item):
    x,y = item
    return y

def filter(cityList, searchString):
    lowerSearchString = searchString.lower()
    result = []
    for city in cityList:
        if lowerSearchString in city['postcode'].lower():
                result.append( (city, True) ) 
                continue

        if lowerSearchString in city['name'].lower():
                result.append( (city, False) )
    return result

@app.route('/get-store-types')
def getStoreTypes():
    storeTypes = []
    for store in stores:
        storeTypes.append(store['shopType'])

    return json.dumps(list(set(storeTypes)))

@app.route('/get-stores-by-type')
def getStoresByType():
    searchByTypeString = request.args.get('searchByTypeString')

    sameTypeStores = [store for store in stores if store['shopType'] == searchByTypeString]

    return json.dumps(sameTypeStores)


    