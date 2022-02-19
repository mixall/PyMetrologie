from sqlalchemy import exc

from app import app
from .models import Location, User, Device


def get_items(model):
    # Vrátí všechny záznamy v tabulce, které odpovídají modelu, řazení A-Z
    return app.session.query(model).order_by(model.name)


def get_items_status(model, status):
    # Vrátí všechny záznamy v tabulce, které odpovídají modelu a statusu, řazení A-Z
    return app.session.query(model).filter(model.status == status).order_by(model.name)


def get_item_by_id(model, item_id):
    # Vrátí první záznam v tabulce, který odpovídá modelu a id
    return app.session.query(model).filter(model.id == item_id).first()


def add_item(item):
    session = False
    while not session:
        try:
            app.session.add(item)
            app.session.commit()
            session = True
        except exc.IntegrityError as e:
            app.session.rollback()


def update_item(item):
    # Aktualizuje zaslaný záznam
    app.session.commit()


def get_form_locations():
    # Vrátí seznam všech záznamů z tabulky Location pro select pole formulářů, řazení ABC
    return get_items(model=Location)


def get_form_users():
    # Vrátí seznam všech záznamů z tabulky User pro select pole formulářů, řazení ABC
    return get_items(model=User)


def get_form_devices():
    # Vrátí seznam všech záznamů z tabulky User pro select pole formulářů, řazení ABC
    return get_items(model=Device)


def get_table_locations():
    # Vrátí všechny záznamy z tabulky Location jako slovník pro vykreslení příslušné tabulky (Table)
    qrs = get_items(model=Location)
    return {qr.id: qr.name for qr in qrs}


def get_table_users():
    # Vrátí všechny záznamy z tabulky User jako slovník pro vykreslení příslušné tabulky (Table)
    qrs = get_items(model=User)
    return {qr.id: qr.name for qr in qrs}


def get_table_devices():
    # Vrátí všechny záznamy z tabulky Device jako slovník pro vykreslení příslušné tabulky (Table)
    qrs = get_items(model=Device)
    return {qr.id: qr.name for qr in qrs}

# # Vrátí seznam všech aktivních lokací + aktuální lokaci zařízení (bez ohledu na to, zda je aktivní či nikoli)
# def location_choice_active(get_id):
#     return app.session.query(Location).filter(
#         or_(Location.status == True, Location.id == get_id)).order_by(Location.name)
#
#
# # Vrátí seznam všech aktivních uživatelů + aktuálního uživatele zařízení (bez ohledu na to, zda je aktivní či nikoli)
# def user_choice_active(get_id):
#     return app.session.query(User).filter(or_(User.status == True, User.id == get_id))
