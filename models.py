import datetime

import borax
from borax.calendars.birthday import actual_age_lunar
from dateutil.relativedelta import relativedelta
from flask import render_template

from exts import db
from borax.calendars.lunardate import LunarDate

today = LunarDate.today()


class FamilyBirthday(db.Model):
    __tablename__ = 'birthday'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.Enum('男', '女'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    zodiac = db.Column(db.Enum("鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"))
    lunar_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


def birth_now(html, days, username):
    years = [0, ]
    for now_year in days:
        birth = now_year[0].replace(year=datetime.datetime.now().year)
        a, b, c = birth.year, birth.month, birth.day
        try:
            lunar_date = LunarDate(a, b, c)
        except borax.calendars.lunardate.InvalidLunarDateError:
            lunar_date = LunarDate(a, b, c - 1)
        now_birth = lunar_date.to_solar_date()
        if today < now_birth:  # 没有过生日
            year = now_birth - today
            years.append(year.days)
        elif today > now_birth:
            year = (now_birth + relativedelta(years=1)) - today
            years.append(year.days)
    ages = [0, ]
    for day in days:
        lunar_date = LunarDate(day[0].year, day[0].month, day[0].day).to_solar_date()
        a = actual_age_lunar(birthday=lunar_date, today=today)
        ages.append(a)
    return render_template(html, data_dict=username, years=ages, days=years)
