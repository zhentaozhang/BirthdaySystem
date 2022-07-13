from flask import Flask, render_template
from models import FamilyBirthday, birth_now
from exts import db
from blueprints import register_bp
from borax.calendars.lunardate import LunarDate
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

today = LunarDate.today()

app.register_blueprint(register_bp)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    username = db.session.query(FamilyBirthday.id, FamilyBirthday.name, FamilyBirthday.lunar_birth).all()
    days = db.session.query(FamilyBirthday.lunar_birth).all()
    db.session.commit()
    return birth_now(html='index.html',days=days, username=username)


@app.route('/music')
def music():
    return render_template('music.html')


if __name__ == '__main__':
    app.run()
