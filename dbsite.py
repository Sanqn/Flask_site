import datetime
import os
import sqlite3
from flask import g, make_response
from flask import Flask, url_for, render_template, request, flash, session, redirect, abort
from dotenv import load_dotenv, find_dotenv
from FBbase import FBbase
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

load_dotenv(find_dotenv())
DATABASE = '/tmp/fldb.db'
UPLOAD_FOLDER = 'img/'


SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fldb.db')))
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'success'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


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
    # op = [('1', 'Main', '/'),
    #       ('2', 'About', 'about'),
    #       ('3', 'Contacts', 'contacts'),
    #       ('4', 'Add post', 'add_post'),
    #       ('5', 'Login', 'login')]
    # query = """INSERT INTO mainmenu(id, name, url) VALUES(?, ?, ?);"""
    # cur.executemany(query, op)
    cur.execute("DELETE FROM posts WHERE id=3;")
    conn.commit()
    conn.close()


dbase = None


@app.before_request
def before_request():
    print('connect')
    global dbase
    db = get_db()
    dbase = FBbase(db)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'link_db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    all_post = dbase.get_all_post()
    if not all_post:
        return render_template('index.html', menu=dbase.menu())
    return render_template('index.html', menu=dbase.menu(), all_post=all_post)
    # content =  render_template('index.html', menu=dbase.menu(), all_post=all_post)
    # res = make_response(content)
    # res.headers['Content-type'] = 'text/plan'
    # res.headers['Server'] = 'flask'
    # return res


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', title='About', menu=dbase.menu())


@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['message']):
            flash('Message sent, thank you!', category='success')
        else:
            flash('You not add text!', category='error')

    print(url_for('contacts'))
    return render_template('contacts.html', title='Contacts', menu=dbase.menu())


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     print(request.form)
#     if 'username' in session:
#         print(request.headers)
#         return redirect(url_for('profile', name=session['username']))
#     elif request.method == 'POST':
#         email = request.form['email']
#         pasw_user = request.form['password']
#         username = dbase.check_user(email, pasw_user)
#         print(username, '=========================')
#         if username:
#             session['username'] = username
#             return redirect(url_for('profile', name=session['username']))
#         else:
#             flash('Data entered incorrectly one', category='error')
#     return render_template('login.html', title='Login', menu=dbase.menu())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userprofile'))
    if request.method == 'POST':
        email = request.form['email']
        username = dbase.getUserbyEmail(email)
        if username and check_password_hash(username['psw'], request.form['password']):
            userLogin = UserLogin().create(username)
            rm = True if request.form.get('rememberme') else False
            login_user(userLogin, remember=rm)
            return redirect(request.args.get('next') or url_for('userprofile'))
        flash('Data entered incorrectly one', category='error')
    return render_template('login.html', title='Login', menu=dbase.menu())

@app.route("/logout1")
@login_required
def logout1():
    logout_user()
    flash('You are logout', category='success')
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if len(request.form['username']) > 2 and request.form['password'] == request.form['repassword']:
            name = request.form['username']
            email = request.form['email']
            hash_psw = generate_password_hash(request.form['password'])
            res = dbase.adduser(name, email, hash_psw)
            if res:
                session['username'] = request.form['username']
                print(session['username'])
                return redirect(url_for('profile', name=session['username']))
            else:
                flash('Email exists or password introduced incorrectly', category='error')
        else:
            flash('Data entered incorrectly', category='error')

    return render_template('registration.html', title='Registration', menu=dbase.menu())


@app.route("/logout")
def logout():
    del session['username']
    return redirect(url_for('index'))


@app.route('/profile/<name>')
def profile(name):
    if 'username' not in session or session['username'] != name:
        abort(401)
    return f'Hi {name}'

@app.route('/userprofile', methods=['GET', 'POST'])
def userprofile():
    id_user = current_user.get_id()
    if request.method == 'POST':
        if current_user.is_authenticated:
            image = request.files['image']
            name_ava = image.filename
            path_to_image = os.path.join(app.config['UPLOAD_FOLDER'], name_ava)
            if name_ava != '':
                ext_image = name_ava.split('.')[-1]
                if ext_image not in ALLOWED_EXTENSIONS:
                    abort(400)
                image.save(os.path.join('static/' + app.config['UPLOAD_FOLDER'], name_ava))
            res = dbase.addava(id_user, path_to_image)
            if not res:
                flash('Ava not save', category='error')
            else:
                flash('Ava added successful', category='success')
    return render_template('userprofile.html', id_user=id_user, title='User_profile', menu=dbase.menu())



@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def addpost():
    if request.method == 'POST':
        if len(request.form['name']) > 2 and len(request.form['text']) > 5:
            print(request.form)
            name_post = request.form['name']
            url_post = request.form['url'].lower()
            text_post = request.form['text']
            image = request.files['image']
            name_image = image.filename
            path_to_image = os.path.join(app.config['UPLOAD_FOLDER'], name_image)
            print(path_to_image)
            if name_image != '':
                ext_image = name_image.split('.')[-1]
                if ext_image not in ALLOWED_EXTENSIONS:
                    abort(400)
                image.save(os.path.join('static/' + app.config['UPLOAD_FOLDER'], name_image))
            res = dbase.addpost(name_post, url_post, text_post, path_to_image)
            if not res:
                flash('Post not save', category='error')
            else:
                flash('Post added successful', category='success')
        else:
            flash('Post not save', category='error')
    return render_template('addpost.html', title='addpost', menu=dbase.menu())


@app.route('/post/<url_post>')
@login_required
def post(url_post):
    article = dbase.get_post(url_post)
    print(dict(article))
    if not article:
        abort(404)
    return render_template('post.html', article=article, title=dict(article)['title'], menu=dbase.menu())


@app.route('/visits-counter')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f'Total visits {session.get("visits")}'


@app.route('/update_data')
def up_data():
    res = str(session.items())

    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['apples'] += 200
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res


@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    session.pop('cart_item', None)  # удаление данных о посещениях
    return 'Visits deleted'


@app.route('/cookie', methods=['GET', 'POST'])
def log():
    if not request.cookies.get('foo'):
        if request.method == 'POST':
            name = request.form['user']
            pas = request.form['pass']
            if name == 'Alex' and pas == 'admin':
                res = make_response(f'Cookies are created')
                res.set_cookie('foo', str((name, pas)), 60 * 60)
                return res
    else:
        res = make_response(f'Cookie is exists {request.cookies.get("foo")}')
        return res
    return render_template('login1.html', title='Cookie', menu=dbase.menu())


@app.route('/kill_cookie')
def kill_cookie():
    res = make_response(f'Cookies are killed')
    res.set_cookie('foo', max_age=0)
    return res


@app.errorhandler(404)
def page_404(error):
    return render_template('page_404.html', title='Error 404', menu=dbase.menu())


def getAvatar():
    ava = (os.path.join('static/' + app.config['UPLOAD_FOLDER'], 'back_ava.png'))
    return ava




if __name__ == '__main__':
    app.run(debug=True)
