from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv
import random
import requests
import json
import config

df = pd.read_csv('netflix_titles.csv', header='infer')
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title_pool = db.Column(db.String())
    def __repr__(self):
        return '<User %r>' % self.id




@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      username = request.form['username']
      # check if username is already taken
      query = Todo.query.filter_by(username=username)
      print(query.count())
      if query.count() == 0:
        # adding new user to db
        session['username'] = username
        new_entry = Todo(username=username, title_pool=json.dumps([]))
        try:
            db.session.add(new_entry)
            db.session.commit()
            print('success adding user')
            return redirect(url_for('index'))
        except:
            return "Problem creating user"

      else:
          # returning or collision in usernames
          session['username'] = username
          return redirect(url_for('index'))
    
    # GET request
    return render_template('login.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'username' in session:
        username = session['username']
        return render_template('about.html', username=username)

    return render_template('about.html')

@app.route('/my_pool', methods=['GET', 'POST'])
def my_pool():
    if request.method == 'POST':
        title = request.form['title']
        user = Todo.query.filter_by(username=session['username']).first()
        try:
            pool_as_list = json.loads(user.title_pool)
            pool_as_list.append(title)
            user.title_pool = json.dumps(pool_as_list)
            db.session.commit()
            return redirect(url_for('my_pool', pool=pool_as_list))
        except:
            return "Error: updating user pool"
    
    if 'username' in session:
        #get user from db and serve the list
        user = Todo.query.filter_by(username=session['username']).first()
        try:
            pool = json.loads(user.title_pool)
            return render_template('my_pool.html', pool=pool)
        except:
            return "Error: getting user pool %s" % user.title_pool
    
    return redirect(url_for('login'))

# User pool functions

@app.route('/delete/title=<id>')
def delete(id):
    user = Todo.query.filter_by(username=session['username']).first()
    try:
        pool_as_list = json.loads(user.title_pool)
        pool_as_list.remove(id)
        user.title_pool = json.dumps(pool_as_list)
        db.session.commit()
        return redirect(url_for('my_pool', pool=pool_as_list))
    except:
        return "Error: deleting title"


# @app.route('/update')
# def update():

@app.route('/my_pool/random')
def select_random_from_pool():
    user = Todo.query.filter_by(username=session['username']).first()
    try:
        pool = json.loads(user.title_pool)
        title = random.choice(pool)
        return render_template('my_pool.html', title=title, pool=pool)
    except:
        return "Error: getting user pool %s" % user.title_pool

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

    if 'username' in session:
        username = session['username']
        return render_template('random_movie.html',movie=movie, username=username)

    return render_template("random_movie.html", movie=movie)
    
if __name__ == "__main__":
    app.run(debug=True, port=4997)