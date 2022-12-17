import sqlite3

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin(name):
    session['admin_logged'] = name


def is_login():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)

menu = [
    {'url': 'index', 'title': 'Main page'},
    {'url': '.index', 'title': 'Admin panel'},
    {'url': '.users', 'title': 'Users'},
    {'url': '.list_articles', 'title': 'All articles'},
    {'url': '.logout', 'title': 'Logout'},
]

db = None
@admin.before_request
def before_request():
    print('connect')
    global db
    db = g.get('con_db')



@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request

@admin.route('/')
def index():
    if not is_login():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Admin panel')

@admin.route('/users')
def users():
    if not is_login():
        return redirect(url_for('.login'))
    list_users = []
    if db:
        query = "SELECT * FROM users ORDER BY time DESC;"
        cur = db.cursor()
        try:
            cur.execute(query)
            list_users = cur.fetchall()
        except sqlite3.Error as e:
            print(f'Error {e}')
        return render_template('admin/users.html', title='Users', menu=menu, list_users=list_users)

@admin.route('/list_articles')
def list_articles():
    if not is_login():
        return redirect(url_for('.login'))
    list_articles = []
    if db:
        query = "SELECT * FROM posts ORDER BY time DESC;"
        cur = db.cursor()
        try:
            cur.execute(query)
            list_articles = cur.fetchall()
        except sqlite3.Error as e:
            print(f'Error {e}')
        return render_template('admin/list_articles.html', title='All posts', menu=menu, list_articles=list_articles)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if is_login():
        print(request.headers)
        return redirect(url_for('.index', name=session['admin_logged']))
    elif request.method == 'POST':
        if request.form['name'] == 'Alex' and request.form['psw'] == 'admin':
            name = request.form['name']
            login_admin(name)
            return redirect(url_for('.index', name=session['admin_logged']))
        else:
            flash('incorrect login/password', category='error')
    return render_template('admin/login_admin.html', title='Admin_panel', menu=menu)


@admin.route('/logout')
def logout():
    if not is_login():
        return redirect(url_for('.login'))
    logout_admin()
    flash('User logout', category='success')
    return redirect(url_for('.login'))


@admin.errorhandler(404)
def page_404(error):
    return render_template('page_404.html', title='Error 404')
