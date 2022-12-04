# import os
#
# from flask import Flask, url_for, render_template, request, flash, session, redirect, abort
# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(find_dotenv())
#
# SECRET_KEY = os.getenv('SECRET_KEY')
# app = Flask(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
#
# menu = [
#     {'name': 'Main', 'url': '/'},
#     {'name': 'About', 'url': 'about'},
#     {'name': 'Contacts', 'url': 'contacts'},
#     {'name': 'Login', 'url': 'login'}
# ]
#
#
# @app.route('/')
# def index():
#     print(url_for('index'))
#     return render_template('index.html', title='Main page', menu=menu)
#
#
# @app.route('/about')
# def about():
#     print(url_for('about'))
#     return render_template('about.html', title='About', menu=menu)
#
#
# @app.route('/contacts', methods=['GET', 'POST'])
# def contacts():
#     if request.method == 'POST':
#         print(request.form)
#         if len(request.form['message']):
#             flash('Message sent, thank you!', category='success')
#         else:
#             flash('You not add text!', category='error')
#
#     print(url_for('contacts'))
#     return render_template('contacts.html', title='Contacts', menu=menu)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     print(request.form)
#     if 'userLogged' in session:
#         return redirect(url_for('profile', name=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'Alex' and request.form['password'] == 'admin':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', name=session['userLogged']))
#     return render_template('login.html', title='Login', menu=menu)
#
#
# @app.route("/logout")
# def logout():
#     del session['userLogged']
#     return redirect(url_for('index'))
#
#
# @app.route('/profile/<name>')
# def profile(name):
#     if 'userLogged' not in session or session['userLogged'] != name:
#         abort(401)
#     return f'Hi {name}'
#
#
# @app.errorhandler(404)
# def page_404(error):
#     return render_template('page_404.html', title='Error 404', menu=menu)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

a = {'name': 'Alex1', 'psw': 'pbkdf2:sha256:260000$msw0MygIb970ucnW$cd3dc708af26a2765947bbb9e5f6e86637d957123245a0da7994b5e6f821dcb5'}


