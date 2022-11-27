import os

from flask import Flask, url_for, render_template, request, flash
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

menu = [
    {'name': 'Main', 'url': '/'},
    {'name': 'About', 'url': 'about'},
    {'name': 'Contacts', 'url': 'contacts'},
    {'name': 'Login', 'url': 'login'}
]


@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', title='Main page', menu=menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='About', menu=menu)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['message']):
            flash('Message sent, thank you!')
        else:
            flash('You not add text!')

    print(url_for('contacts'))
    return render_template('contacts.html', title='Contacts', menu=menu)


@app.route('/profile/<name>')
def profile(name):
    print(url_for('profile', name='San'))
    return f'Hi {name}'


if __name__ == '__main__':
    app.run(debug=True)
