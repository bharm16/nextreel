from flask import Flask, render_template
import requests
from urllib.parse import quote
import os

app = Flask(__name__)


@app.route('/')
def home():
    response = requests.get('https://imdb-api.com/en/API/SearchMovie/k_0vtefojw/fim')
    data = response.json()
    return render_template('home.html', movies=data['movies'])


if __name__ == '__main__':
    app.run(debug=True)
