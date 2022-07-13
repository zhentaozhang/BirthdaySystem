import datetime

import borax
from borax.calendars.birthday import actual_age_lunar
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, flash, render_template
from exts import db
from models import FamilyBirthday, birth_now
from borax.calendars.lunardate import LunarDate

bp = Blueprint('register', __name__, url_prefix='/birth')
today = LunarDate.today()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        zodiac = request.form.get('zodiac')
        lunar_birth = request.form.get('lunar_birth')
        phone_number = request.form.get('phone_number')
        if zodiac not in ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]:
            flash('输入生肖有误')
        elif sex not in ['男', '女']:
            flash("输入性别有误")
        else:
            new_user = FamilyBirthday(name=name, sex=sex, age=age, zodiac=zodiac, lunar_birth=lunar_birth,
                                      phone_number=phone_number)

            db.session.add(new_user)
            db.session.commit()
            return ''
    return render_template('register.html')


@bp.route('/ditail/<int:detail_id>', methods=['GET', 'POST'])
def detail(detail_id):
    username = db.session.query(FamilyBirthday.id, FamilyBirthday.name, FamilyBirthday.sex, FamilyBirthday.lunar_birth,
                                FamilyBirthday.zodiac, FamilyBirthday.phone_number).filter(
        FamilyBirthday.id == detail_id).all()
    days = db.session.query(FamilyBirthday.lunar_birth).filter(FamilyBirthday.id == detail_id).first()[0]
    lunar_date = LunarDate(days.year, days.month, days.day).to_solar_date()
    age = actual_age_lunar(birthday=lunar_date, today=today)
    birth = days.replace(year=datetime.datetime.now().year)
    a, b, c = birth.year, birth.month, birth.day
    try:
        lunar_date = LunarDate(a, b, c)
    except borax.calendars.lunardate.InvalidLunarDateError:
        lunar_date = LunarDate(a, b, c - 1)
    now_birth = lunar_date.to_solar_date()
    if today < now_birth:  # 没有过生日
        year = now_birth - today
    elif today > now_birth:
        year = (now_birth + relativedelta(years=1)) - today
    return render_template('user.html', data_dict=username, age=age, year=year.days)


@bp.route('/search')
def search():
    q = request.args.get('q')
    search_name = db.session.query(FamilyBirthday.id, FamilyBirthday.name, FamilyBirthday.lunar_birth).filter(
        FamilyBirthday.name.contains(q))
    days = db.session.query(FamilyBirthday.lunar_birth).all()
    return birth_now(html='index_search.html',days=days, username=search_name)
