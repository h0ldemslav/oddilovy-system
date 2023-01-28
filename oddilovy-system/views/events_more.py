from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_mail import Message

import auth
import forms


from service.user_service import UserService
from service.event_service import EventService

events_more = Blueprint('events_more', __name__)

@events_more.route('/')
@auth.login_required
def view_events_page():
    import app

    akce = EventService.get_all_events_with_program()
    druziny = EventService.get_all_events_with_druzina()
    je_prihlaseno_dite, deti, dochazka, child_id = None, None, None, None
    child_name = ''

    if session['role'] not in ('vedouci', 'administrator'):
        akce = list(filter(lambda zaznam: zaznam['je_public'] == 1, akce))

        if session['role'] == 'rodic':
            child_id = request.args.get('child_id', None, int)
            deti = UserService.get_children_by_parent(session['id'])
            id_event = request.args.get('id_event', None, int)

            if child_id is None and len(deti) > 0:
                child_id = deti[0]['id_user']

            if child_id is not None and len(deti) > 0:
                child_name = UserService.get_user_by_id(child_id)['jmeno'] + ' ' + UserService.get_user_by_id(child_id)[
                    'prijmeni']

            dojde = request.args.get('dojde', default=False, type=lambda v: v.lower() == 'true')

            if dojde is not None and id_event is not None:
                EventService.change_dochazka(dojde, child_id, id_event)
                if dojde:
                    flash('Uživatel ' + child_name + ' byl úspěšně přihlášen na akci')
                else:
                    flash('Uživatel ' + child_name + ' byl úspěšně odhlášen z akce')

            if id_event is not None:
                dochazka = EventService.get_dochazka_by_user_and_akce_id(child_id, id_event)

        if session['role'] == 'dite':
            je_prihlaseno_dite = EventService.get_dochazka_by_user_and_akce_id(session['id'], akce[0]['id_akce'])
            je_prihlaseno_dite = False if je_prihlaseno_dite == None else je_prihlaseno_dite['dochazka']

            if je_prihlaseno_dite and request.args != {}:
                special_proposition = ''.join(['- ' + food + '\n' for food in request.args.values()])
                msg = Message('Zpráva z webu 1oddilorli', sender=session['email'],
                              recipients=['martinacek.n@gmail.com'])
                msg.body = f"{'Jméno a příjmění: ' + session['name']}\nSpeciální propozice:\n{special_proposition}"
                app.mail.send(msg)
                flash('Nabídka byla odeslána vedoucímu')

    elif session['role'] in ('vedouci', 'administrator') and request.args.get('id_akce'):
        EventService.set_public(request.args.get('id_akce'))
        flash('Akce byla zveřejněna')
        return redirect(url_for('events_more.view_events_page'))

    return render_template('events_page_more.jinja', akce=akce, druziny=druziny, deti=deti,
                           child_name=child_name,
                           dochazka=dochazka, child_id=child_id, je_prihlaseno_dite=je_prihlaseno_dite)

@events_more.route('/edit', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('vedouci', 'administrator')
def edit_event():
    edit_form = forms.NewBigEventForm(request.form)
    akce = dict(EventService.get_event_by_id(request.args.get('id_akce')))
    edit_form.jmeno.data = akce['jmeno']
    edit_form.misto.data = akce['misto']
    edit_form.popis.data = akce['popis']

    if request.method == 'POST':
        akce_data = [request.form.get('jmeno'), request.form.get('datum'), request.form.get('misto'),
            request.form.get('zacatek_akce'), request.form.get('konec_akce'), request.form.get('popis'),
            int(akce['id_akce'])]
        EventService.update_event_by_id(akce_data)
        flash('Akce byla upravena')
        return redirect(url_for('events_more.view_events_page'))

    return render_template('events_edit_page.jinja', edit_form=edit_form)

@events_more.route('/delete/')
@auth.login_required
@auth.roles_required('vedouci', 'administrator')
def delete_event():
    EventService.delete_event_by_id(request.args.get('id_akce'))
    flash('Akce byla vymazána')
    return redirect(url_for('events_more.view_events_page'))


@events_more.route('/attendance/', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('vedouci', 'administrator')
def view_attendance_page():
    children = UserService.get_all_children_by_event(request.args.get('id_akce'))

    if request.method == 'POST':
        id_akce = request.args.get('id_akce')
        form_list = dict(request.form.lists())
        form_list = list(form_list.values())
        index = 0

        while (index != len(form_list)):
            dochazka = form_list[index][0]
            index += 1

            id_user = form_list[index][0]
            index += 1

            duvod = form_list[index][0] if form_list[index][0] is not None else ''
            index += 1

            EventService.change_dochazka(dochazka, id_user, id_akce, duvod)

        flash('Docházka byla odeslána')
        return redirect(url_for('events_more.view_events_page'))

    return render_template('attendance_page.jinja',
                           children=children, id_akce=request.args.get('id_akce'),
                           jmeno_akce=request.args.get('jmeno_akce'))
