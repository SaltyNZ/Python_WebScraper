from flask import Flask, render_template, request, jsonify
import WebScraper as SP
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/data', methods=['GET'])
def getData():
    listings = []
    if 'category' in request.args:
        category = request.args['category']
        listings = SP.getList('https://www.nzdirectory.co.nz/{}.html'.format(category), 'https://www.nzdirectory.co.nz/')
    return render_template("table.html", listings=listings)