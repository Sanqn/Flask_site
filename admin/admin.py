from flask import Blueprint, render_template, request, redirect, url_for, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin(name):
    session['admin_logged'] = name


def is_login():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)

menu = [
    {'url': '.index', 'title': 'Admin panel'},
    {'url': '.logout', 'title': 'Logout'},
]

@admin.route('/')
def index():
    if not is_login():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Admin panel')


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
    return render_template('admin/login_admin.html', title='Admin_panel')


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
