from flask import Blueprint, render_template, request, flash, redirect, url_for

import auth
import forms

from service.user_service import UserService
from service.program_service import ProgramService
from service.druzina_service import DruzinaService
from service.druzina_service import NovaDruzinaService
from service.event_service import EventService

admin = Blueprint('admin', __name__)

@admin.route('/registrace', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('administrator')
def view_admin_registration_page():
    form = forms.RegistrationForm(request.form)
    druziny = DruzinaService.get_all()
    rodice = UserService.get_all_parents()
    form.id_druzina_clenem.choices = [(item['id_druzina'], item['jmeno']) for item in druziny]
    form.id_druzina_clenem.choices.append((None, 'neni clenem'))
    form.id_druzina_vede.choices = [(item['id_druzina'], item['jmeno']) for item in druziny]
    form.id_druzina_vede.choices.append((None, 'nevede druzinu'))
    form.id_rodice.choices = [(item['id_user'], item['jmeno'] + ' ' + item['prijmeni']) for item in rodice]
    form.id_rodice.choices.append((None, 'nema rodice'))

    if request.method == 'POST':
        UserService.register_user(
            login=request.form['login'],
            heslo=request.form['heslo'],
            rodne_cislo=request.form['rodne_cislo'],
            jmeno=request.form['jmeno'],
            prijmeni=request.form['prijmeni'],
            adresa=request.form['adresa'],
            telefon=request.form['telefon'],
            email=request.form['email'],
            datum_narozeni=request.form['datum_narozeni'],
            id_rodice=request.form['id_rodice'],
            id_role=request.form['id_role'],
            id_druzina_vede=request.form['id_druzina_vede'],
            id_druzina_clenem=request.form['id_druzina_clenem']
        )
        flash('Uspesne zaregistrovano')
    return render_template('admin_registration_page.jinja', register_form=form)

@admin.route('/programs')
@auth.login_required
@auth.roles_required('administrator')
def view_admin_programs_page():
    return render_template('admin_programs_page.jinja')

@admin.route('/newprogram', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('administrator')
def view_admin_newprogram_page():
    form = forms.NewProgramForm(request.form)
    if request.method == 'POST':
        ProgramService.new_program(
            misto=request.form['misto_programu'],
            popis=request.form['popis'],
            delka=request.form['delka'],
            doporuceny_vek=request.form['doporuceny_vek']
        )
        flash('Akce přidána')
    return render_template('admin_newprogram_page.jinja', newprogram_form=form)

@admin.route('/newbigevent', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('administrator')
def view_admin_newbigevent_page():
    form = forms.AkceSProgramemForm(request.form)
    druziny = DruzinaService.get_all()
    form.druzina.choices = [(item['id_druzina'], item['jmeno']) for item in druziny]
    vedouci = UserService.get_vsechny_vedouci()
    form.vedouci.choices = [(item['id_user'], item['prijmeni']) for item in vedouci]
    if request.method == 'POST':
        ProgramService.new_program(
            misto=request.form['misto_programu'],
            popis=request.form['popis_programu'],
            delka=request.form['delka'],
            doporuceny_vek=request.form['doporuceny_vek']
        )
        EventService.new_big_event(
            jmeno=request.form['jmeno'],
            datum=request.form['datum'],
            misto=request.form['misto'],
            zacatek_akce=request.form['zacatek_akce'],
            konec_akce=request.form['konec_akce'],
            popis=request.form['popis'],
            druzina=form.druzina.data,
            vedouci=form.vedouci.data
        )
        flash('Akce s programem přidána')
    return render_template('admin_newbigevent_page.jinja', form=form)

@admin.route('/newgroup', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('administrator')
def view_admin_newgroup_page():
    form = forms.NewGroupForm(request.form)

    if request.method == 'POST':
        NovaDruzinaService.new_group(
            request.form['jmeno'],
            request.form['vek'],
            request.form['popis']
        )
        flash('Nová skupina byla založena')

    return render_template('admin_newgroup_page.jinja', form=form)

@admin.route('/showprograms')
@auth.login_required
@auth.roles_required('administrator')
def view_admin_showprograms_page():
    programs = ProgramService.get_all_programs()
    return render_template('admin_showprograms_page.jinja',program=programs)

@admin.route('/edit_program',methods=['GET','POST'])
@auth.login_required
@auth.roles_required('administrator')
def edit_program():
    edit_form = forms.NewProgramForm(request.form)
    program = dict(ProgramService.get_program_by_id(request.args.get('id_program')))
    edit_form.misto_programu.data = program['misto_program']
    edit_form.popis.data = program['popis_program']
    edit_form.delka.data = program['delka']
    edit_form.doporuceny_vek.data = program['doporuceny_vek']
    if request.method == 'POST':
        program_data = [request.form.get('misto_programu'), request.form.get('popis'), request.form.get('delka'), request.form.get('doporuceny_vek'),
        int(program['id_program'])]
        ProgramService.update_program_by_id(program_data)
        flash('Program byl upraven')
        return redirect(url_for('admin.view_admin_showprograms_page'))
    return render_template('admin_programchanges_page.jinja',edit_form=edit_form)

@admin.route('/delete_program/<int:id>')
@auth.login_required
@auth.roles_required('administrator')
def delete_program(id):
    ProgramService.delete_program_with_id(id)
    flash('Program byl smazán')
    return redirect(url_for('admin.view_admin_showprograms_page'))