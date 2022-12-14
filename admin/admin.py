from flask import Blueprint, render_template, request, redirect, url_for, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1

def is_login():
    return True if session.get('admin_logged') else False

def logout():
    session.pop('admin_logged', None)



@admin.route('/')
def index():
    return 'admin'


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['name'] == 'Admin' and request.form['psw'] == 'admin':
            login_admin()
            flash('User login', category='success')
            return redirect(url_for('.index'))
        else:
            flash('incorrect login/password', category='error')
    return render_template('admin/login_admin.html', title='Admin_panel')


@admin.errorhandler(404)
def page_404(error):
    return render_template('page_404.html', title='Error 404')
