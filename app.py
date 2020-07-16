from flask import Flask, render_template, url_for, redirect
import csv
import random
import requests
import config


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/random')
def select_random():

    # randomly select a movie
    with open('netflix_titles.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        row = random.choice(list(reader))
    
    movie = {
        'id': row[0],
        'category': row[1],
        'title': row[2],
        'director': row[3],
        'cast': row[4],
        'country': row[5],
        'date_added': row[6],
        'release_year': row[7],
        'rating': row[8],
        'duration': row[9],
        'genre': row[10],
        'description': row[11],
        # default
        'image': 'https://live.staticflickr.com/4422/36193190861_93b15edb32_z.jpg',
        'imdb': 'Not Available'
   }

    # fetch cover image
    url = f"http://www.omdbapi.com/?t={movie['title']}/&apikey={config.api_key}"
    # get back the response
    response = requests.request("GET", url)
    # parse result into JSON and look for matching data if available
    movie_data = response.json()
    if 'Poster' in movie_data:
        movie['image'] = movie_data['Poster']
    if 'imdbRating' in movie_data:
        movie['imdb'] = movie_data['imdbRating']
    # send all this data to the index.html template
    return render_template("index.html", movie=movie)
    
if __name__ == "__main__":
    app.run(debug=True)