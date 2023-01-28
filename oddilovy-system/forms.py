from wtforms import Form, IntegerField, StringField, SelectField, PasswordField, validators, DateField, TextAreaField, SelectMultipleField

class SignForm(Form):
    login = StringField(name='login', label='', validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='', validators=[validators.length(min=6), validators.InputRequired()])

class RegistrationForm(Form):
    login = StringField(name='login', label='Login', validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    heslo = PasswordField(name='heslo', label='Heslo', validators=[validators.length(min=6), validators.InputRequired()])
    rodne_cislo = StringField(name='rodne_cislo', label= 'Rodné číslo', validators=[validators.InputRequired()])
    jmeno = StringField(name='jmeno', label='Jméno', validators=[validators.InputRequired()])
    prijmeni = StringField(name='prijmeni', label='Příjmení', validators=[validators.InputRequired()])
    adresa = StringField(name='adresa', label='Adresa', validators=[validators.InputRequired()])
    telefon = IntegerField(name='telefon', label='Telefon', validators=[validators.Length(min=8), validators.InputRequired()])
    email = StringField(name='email', label='Email', validators=[validators.InputRequired()])
    datum_narozeni = StringField(name='datum_narozeni', label='Datum narození', validators=[validators.InputRequired()])
    id_rodice = SelectField(name='id_rodice', label='Rodič', choices=[])
    id_role = SelectField(name='id_role', label='Role', choices=[(1, 'administrator'), (2, 'vedouci'), (3, 'rodic'), (4, 'dite')])
    id_druzina_vede = SelectField(name='id_druzina_vede', label='Vede družinu', choices=[])
    id_druzina_clenem = SelectField(name='id_druzina_clenem', label='Členem družiny', choices=[])

class NewProgramForm(Form):
    misto_programu = StringField(name='misto_programu', label='Místo', validators=[validators.Length(max=50), validators.InputRequired()])
    popis = StringField(name='popis', label='Popis', validators=[validators.Length(max=200), validators.InputRequired()])
    delka = StringField(name='delka', label='Délka', validators=[validators.Length(max=30), validators.InputRequired()])
    doporuceny_vek = IntegerField(name='doporuceny_vek', label='Doporučený věk')

class NewBigEventForm(Form):
    jmeno = StringField(name='jmeno', label='Název akce', validators=[validators.Length(max=30), validators.InputRequired()])
    datum = DateField(name='datum', label='Datum akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    misto = StringField(name='misto', label='Místo', validators=[validators.Length(max=50), validators.InputRequired()])
    zacatek_akce = DateField(name='zacatek_akce', label='Začátek akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    konec_akce = DateField(name='konec_akce', label='Konec akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    popis = StringField(name='popis', label='Popis', validators=[validators.Length(max=200)])

class NewGroupForm(Form):
    jmeno = StringField(name='jmeno', label='Název družiny', validators=[validators.Length(max=30), validators.InputRequired()])
    nejmladsi_vek = IntegerField(name='vek', label='Nejmladší věk', validators=[validators.InputRequired()])
    popis = StringField(name='popis', label='Popis družiny', validators=[validators.Length(max=200)])

class EmailForm(Form):
    email = StringField(name='email', label='E-mail', validators=[validators.Length(max=50), validators.InputRequired()])
    zprava = TextAreaField(name='zprava', label='Zpráva', validators=[validators.Length(max=500), validators.InputRequired()])

class AkceSProgramemForm(Form):
    jmeno = StringField(name='jmeno', label='Název akce', validators=[validators.Length(max=30), validators.InputRequired()])
    datum = DateField(name='datum', label='Datum akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    misto = StringField(name='misto', label='Místo', validators=[validators.Length(max=50), validators.InputRequired()])
    zacatek_akce = DateField(name='zacatek_akce', label='Začátek akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    konec_akce = DateField(name='konec_akce', label='Konec akce', format='%d/%m/%Y', validators=[validators.InputRequired()])
    popis = StringField(name='popis', label='Popis', validators=[validators.Length(max=200)])

    misto_programu = StringField(name='misto_programu', label='Místo programu', validators=[validators.Length(max=50), validators.InputRequired()])
    popis_programu = StringField(name='popis_programu', label='Popis', validators=[validators.Length(max=200), validators.InputRequired()])
    delka = StringField(name='delka', label='Délka', validators=[validators.Length(max=30), validators.InputRequired()])
    doporuceny_vek = IntegerField(name='doporuceny_vek', label='Doporučený věk')

    druzina = SelectMultipleField(name='druzina', label='Družina', choices=[], validators=[validators.InputRequired()])
    vedouci = SelectMultipleField(name='vedouci', label='Vedoucí', choices=[], validators=[validators.InputRequired()])