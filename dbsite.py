import os
import sqlite3
from flask import g

from flask import Flask, url_for, render_template, request, flash, session, redirect, abort
from dotenv import load_dotenv, find_dotenv
from FBbase import FBbase

load_dotenv(find_dotenv())

DATABASE = '/tmp/fldb.db'

SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fldb.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def insert_data_in_table():
    conn = connect_db()
    cur = conn.cursor()
    op = [('1', 'Main', '/'),
          ('2', 'About', 'about'),
          ('3', 'Contacts', 'contacts'),
          ('4', 'Add post', 'add_post'),
          ('5', 'Login', 'login')]
    query = """INSERT INTO mainmenu(id, name, url) VALUES(?, ?, ?);"""
    cur.executemany(query, op)
    # cur.execute("DELETE FROM menu;")
    conn.commit()
    conn.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'link_db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    db = get_db()
    dbase = FBbase(db)
    all_post = dbase.get_all_post()
    return render_template('index.html', menu=dbase.menu(), all_post=all_post)


@app.route('/about')
def about():
    db = get_db()
    dbase = FBbase(db)
    print(url_for('about'))
    return render_template('about.html', title='About', menu=dbase.menu())


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    db = get_db()
    dbase = FBbase(db)
    if request.method == 'POST':
        print(request.form)
        if len(request.form['message']):
            flash('Message sent, thank you!', category='success')
        else:
            flash('You not add text!', category='error')

    print(url_for('contacts'))
    return render_template('contacts.html', title='Contacts', menu=dbase.menu())


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    dbase = FBbase(db)
    print(request.form)
    if 'userLogged' in session:
        return redirect(url_for('profile', name=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Alex' and request.form['password'] == 'admin':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', name=session['userLogged']))
    return render_template('login.html', title='Login', menu=dbase.menu())


@app.route("/logout")
def logout():
    del session['userLogged']
    return redirect(url_for('index'))


@app.route('/profile/<name>')
def profile(name):
    if 'userLogged' not in session or session['userLogged'] != name:
        abort(401)
    return f'Hi {name}'


@app.route('/add_post', methods=['GET', 'POST'])
def addpost():
    db = get_db()
    dbase = FBbase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 2 and len(request.form['text']) > 5:
            print(request.form)
            name_post = request.form['name']
            text_post = request.form['text']
            res = dbase.addpost(name_post, text_post)
            if not res:
                flash('Post not save', category='error')
            else:
                flash('Post added successful', category='success')
        else:
            flash('Post not save', category='error')
    return render_template('addpost.html', title='addpost', menu=dbase.menu())


@app.route('/post/<int:id_post>')
def post(id_post):
    db = get_db()
    dbase = FBbase(db)
    article = dbase.get_post(id_post)
    print(article)
    if not article:
        abort(404)
    return render_template('post.html', article=dict(article), title=dict(article)['title'],  menu=dbase.menu())


@app.errorhandler(404)
def page_404(error):
    db = get_db()
    dbase = FBbase(db)
    return render_template('page_404.html', title='Error 404', menu=dbase.menu())


if __name__ == '__main__':
    app.run(debug=True)
