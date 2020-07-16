from flask import Flask, render_template, url_for, redirect, request, session
import pandas as pd
import csv
import random
import requests
import config

df = pd.read_csv('netflix_titles.csv', header='infer')
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/my_pool')
def my_pool():
    # if request.method == 'POST':
    #     # movies_selected = request.form.getlist('movies')
    #     # movies_selected = request.form['movies']
    #     # print(str(movies_selected))
    #     # print(request.form['movie_selected'])
    #     return redirect('/about')
    
    if 'username' in session:
        return render_template('my_pool.html')
    
    return redirect(url_for('login'))

@app.route('/random')
def select_random():
    # randomly select a movie
    row = df.sample()
    
    movie = {
        'id': row['show_id'].values[0],
        'category': row['type'].values[0],
        'title': row['title'].values[0],
        'director': row['director'].values[0],
        'cast': row['cast'].values[0],
        'country': row['country'].values[0],
        'date_added': row['date_added'].values[0],
        'release_year': row['release_year'].values[0],
        'rating': row['rating'].values[0],
        'duration': row['duration'].values[0],
        'genre': row['listed_in'].values[0],
        'description': row['description'].values[0],
        # default image
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
    app.run(debug=True, port=4996)