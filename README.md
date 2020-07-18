# Netflix Randomizer
https://title-randomizer.herokuapp.com/


## Description
Main feature of this website is being able to pull random Netflix title from a dataset of over 6,000 titles. Another feature is being able to create custom title pools and the website will then give you a random title from your own pool. The pools entered here are collected into a database for personal use which I intend to use for a recommender system.


This project was accomplished using Flask, SQLAlchemy with SQLite, and Bootstrap for a quick cycle from concept to deployment on Heroku.

## Learn More
I used a free data set from Kaggle which can be found <a href="https://www.kaggle.com/shivamb/netflix-shows">here</a>.


I used the RESTful API known as OMDB to fill in information that was missing from the data set from Kaggle and can be found <a href="http://www.omdbapi.com/">here</a>. It is completely free to use and keys are issued quickly.