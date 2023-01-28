from flask import Blueprint, render_template, session, flash, request, redirect, url_for

import auth
import forms

from service.user_service import UserService

login = Blueprint('login', __name__)

@login.route('/signin', methods=['GET', 'POST'])
def view_sign_in_page():
    form = forms.SignForm(request.form)
    if request.method == 'POST':
        user = UserService.verify(login=request.form['login'], password=request.form['password'])
        if not user:
            flash('Nespravne heslo nebo login')
        else:
            session['authenticated'] = 1
            session['id'] = user['id_user']
            session['id_druziny'] = user['id_druzina_clenem']
            session['name'] = user['jmeno'] + ' ' + user['prijmeni']
            session['login'] = user['login']
            session['email'] = user['email']
            session['role'] = user['nazev']
            return redirect(url_for('unregistered_user.view_home_page'))

    return render_template('sign_in.jinja', sign_in_form = form)

@login.route('/signout')
@auth.login_required
def signout():
    session.pop('authenticated')
    session.pop('id')
    session.pop('id_druziny')
    session.pop('name')
    session.pop('login')
    session.pop('email')
    session.pop('role')
    return redirect(url_for('unregistered_user.view_home_page'))