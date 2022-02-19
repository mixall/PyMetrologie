from flask_table import Table, Col, LinkCol, BoolCol, OptCol
from flask import url_for
from app.db.crud import get_table_locations, get_table_users, get_table_devices


class UserTable(Table):
    # border = True
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    no_items = 'Seznam je prázdný'
    id = Col('Id', show=True)
    name = LinkCol('Jméno', 'user_detail', 'name', url_kwargs=dict(item_id='id'))
    email = Col('E-mail')
    status = BoolCol('Stav', yes_display='Aktivní', no_display='Neaktivní')
    change_date = Col('Poslední změna', show=False)


class LocationTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    no_items = 'Seznam je prázdný'
    id = Col('Id', show=True)
    name = LinkCol('Název', 'location_detail', 'name', url_kwargs=dict(item_id='id'))
    address = Col('Adresa')
    status = BoolCol('Stav', yes_display='Aktivní', no_display='Neaktivní')
    change_date = Col('Poslední změna', show=False)


class DeviceTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    no_items = 'Seznam je prázdný'
    id = Col('Id', show=True)
    name = LinkCol('Název', 'device_detail', 'name', url_kwargs=dict(item_id='id'))
    type = Col('Typ')
    ns = Col('Nákladové středisko')
    location_id = OptCol('Lokace', choices=get_table_locations())
    user_id = OptCol('Uživatel', choices=get_table_users())
    note = Col('Poznámka k zařízení')
    # user_id = OptCol('Uživatel', choices={1: "test"})
    status = BoolCol('Stav', yes_display='Aktivní', no_display='Neaktivní')
    change_date = Col('Poslední změna', show=False)

    # allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('device_list', sort=col_key, direction=direction)


class MeterTable(Table):
    classes = ['table-sm', 'table-striped', 'table-bordered']
    no_items = "Seznam je prázdný"
    id = Col('Id', show=True)
    name = LinkCol('Výrobní číslo', 'meter_detail', 'name', url_kwargs=dict(item_id='id'))
    model = Col('Model')
    act_dev_id = OptCol("Akt. zařízení", choices=get_table_devices())
    act_dev_detail = Col("Poznámka k akt. zařízení")
    home_dev_status = BoolCol("Zápůjčka", yes_display='Ano', no_display='Ne')
    home_dev_id = OptCol("Dom. zařízení", choices=get_table_devices())
    #ns = Col("Nákladové středisko")
    #location_id = OptCol("Lokace", choices=location_dict())
    #user_id = OptCol("Uživatel", choices=user_dict())
    #note = Col("Poznámka k zařízení")
    # user_id = OptCol("Uživatel", choices={1: "test"})
    status = BoolCol('Stav', yes_display='Aktivní', no_display='Neaktivní')

    # change_date = Col("Poslední změna", show=False)
    # allow_sort = True
