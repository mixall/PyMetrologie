from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, SubmitField, HiddenField, TextAreaField, validators
from wtforms_sqlalchemy.fields import QuerySelectField
from app.db import models


class AddUserForm(FlaskForm):
    id = HiddenField()
    name = StringField(u"Jméno uživatele",
                       validators=[validators.InputRequired(),
                                   validators.Length(min=3, max=50,
                                                     message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                       render_kw={"placeholder": "Zadej jméno uživatele"})
    email = StringField(u"E-mail uživatele",
                        validators=[validators.InputRequired(),
                                    validators.Email(message="Neplatná emailová adresa"),
                                    validators.Length(min=3, max=50,
                                                      message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                        render_kw={"placeholder": "Zadej e-mail uživatele"})
    status = HiddenField()
    change_date = HiddenField()
    submit = SubmitField(u"Přidat záznam")


class AddLocationForm(FlaskForm):
    id = HiddenField()
    name = StringField(u"Název lokace",
                       validators=[validators.InputRequired(),
                                   validators.Length(min=3, max=50,
                                                     message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                       render_kw={"placeholder": "Zadej název lokace"})
    address = StringField(u"Adresa lokace",
                          validators=[validators.InputRequired(),
                                      validators.Length(min=3, max=150,
                                                        message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                          render_kw={"placeholder": "Zadej adresu lokace"})
    status = HiddenField()
    change_date = HiddenField()
    submit = SubmitField(u"Přidat záznam")


class AddDeviceForm(FlaskForm):
    id = HiddenField()
    name = StringField(u"Název zařízení",
                       validators=[validators.InputRequired(),
                                   validators.Length(min=3, max=50,
                                                     message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                       render_kw={"placeholder": "Zadej název zařízení"})
    type = SelectField(u"Typ zařízení",
                       validators=[validators.InputRequired()],
                       choices=models.DeviceTypeEnum,
                       render_kw={"placeholder": "Zadej typ zařízení"})
    # ns = nákladové středisko, zatím validace 1-5 znaků, správně přesně 5
    ns = StringField(u"Nákladové středisko",
                     validators=[validators.InputRequired(),
                                 validators.Length(min=1, max=5,
                                                   message="Nesprávná délka (musí být %(min)d - %(max)d znaků)")],
                     render_kw={"placeholder": "Zadej nákladové středisko"})
    location_id = QuerySelectField(u'Lokace',
                                   validators=[validators.DataRequired(message="Povinný údaj")],
                                   get_label=lambda x: x.name + " (" + x.return_status() + ") ",
                                   allow_blank=True,
                                   blank_text="Vyber lokaci")
    user_id = QuerySelectField(u'Uživatel',
                               validators=[validators.DataRequired(message="Povinný údaj")],
                               get_label=lambda x: x.name + " (" + x.return_status() + ") ",
                               allow_blank=True,
                               blank_text="Vyber uživatele")
    note = TextAreaField(u"Poznámka", render_kw={"placeholder": "Poznámka"})
    status = HiddenField()
    change_date = HiddenField()
    submit = SubmitField(u"Přidat záznam")


class AddMeterForm(FlaskForm):
    id = HiddenField()
    name = StringField(u"Výrobní číslo",
                       validators=[validators.InputRequired(),
                                   validators.Length(min=3, max=25,
                                                     message="Nesprávná délka (min. %(min)d, max. %(max)d znaků)")],
                       render_kw={"placeholder": "Zadej výrobní číslo měřidla"})
    model = SelectField(u"Model",
                        validators=[validators.InputRequired()],
                        choices=models.MeterModelEnum,
                        render_kw={"placeholder": "Zadej model měřidla"})
    act_dev_id = QuerySelectField(u"Aktuální zařízení",
                                  validators=[validators.DataRequired(message="Povinný údaj")],
                                  get_label=lambda x: x.name + " (" + x.return_status() + ") ",
                                  allow_blank=True,
                                  blank_text="Vyber aktuální zařízení")
    act_dev_detail = TextAreaField(u"Poznámka k aktuálnímu zařízení",
                                   validators=[validators.Length(min=0, max=25,
                                                                 message="Nesprávná délka, max. %(max)d znaků)")],
                                   render_kw={"placeholder": "Zadej poznámku k akt. zařízení"})
    home_dev_status = BooleanField(u"Zápůjčka", render_kw={"onchange": "doStuff()"})
    home_dev_id = QuerySelectField(u"Dom. zařízení",
                                   get_label=lambda x: x.name + " (" + x.return_status() + ") ",
                                   allow_blank=True,
                                   blank_text="Vyber domovské zařízení (při zápůjčce)")
    status = HiddenField()
    change_date = HiddenField()
    submit = SubmitField(u"Přidat záznam")

    def home_dev(self):
        if self.home_dev_status.data:
            return self.home_dev_id.data.id
        else:
            return self.act_dev_id.data.id
