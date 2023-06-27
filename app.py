from flask import Flask
from flask_mail import Mail

from views.admin import admin
from views.events_more import events_more
from views.login import login
from views.unregistered_user import unregistered_user

from database import database

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'martinacek.n@gmail.com'
app.config['MAIL_PASSWORD'] = 'jkmgfeinzfzemjdd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.register_blueprint(login, url_prefix='')
app.register_blueprint(events_more, url_prefix='/events_more')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(unregistered_user, url_prefix='')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)