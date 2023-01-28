from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_mail import Message

import auth
import forms

from service.user_service import UserService

unregistered_user = Blueprint('unregistered_user', __name__)

@unregistered_user.route('/')
def view_home_page():
    return render_template('home_page.jinja')

@unregistered_user.route('/events')
def view_meetings_page():
    return render_template('events_page.jinja')

@unregistered_user.route('/contacts', methods=['GET', 'POST'])
def view_contacts_page():
    from app import mail
    form = forms.EmailForm(request.form)
    if request.method == 'POST':
        msg = Message('Zpráva z webu 1oddilorli', sender=request.form['email'], recipients=['martinacek.n@gmail.com'])
        msg.body = f"E-mail odesílatele: {request.form['email']}\nObsah zprávy:\n{request.form['zprava']}"
        mail.send(msg)
        flash('Mail odeslán')
        return redirect(url_for('unregistered_user.view_contacts_page'))
    return render_template('contacts_page.jinja', email_form = form)

@unregistered_user.route('/personal_page')
@auth.login_required
def view_personal_page():
    user_personal_data = UserService.get_user_by_id(session['id'])
    deti=None

    if session['role'] == 'rodic':
        deti = UserService.get_children_by_parent(session['id'])

    return render_template('personal_page.jinja', user_personal_data=user_personal_data, deti=deti)
