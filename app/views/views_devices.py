from datetime import datetime
from flask import request, render_template, flash, url_for, redirect
from sqlalchemy import text

from app import app
from app.views.tables import DeviceTable, LinkCol
from app.views.forms import AddDeviceForm
from app.db.models import Device, Location, User
from app.db import crud


@app.route("/device/?filters=<filters>")
@app.route("/device/")
def device_list(filters="active"):
    # Stránka se seznamem záznamů
    status = False if filters == "inactive" else True
    devices = crud.get_items_status(model=Device, status=status)
    table = DeviceTable(devices)
    if status:
        table.add_column('status_change',
                         LinkCol('Deaktivovat', 'device_status', url_kwargs=dict(item_id="id")))
    else:
        table.add_column('status_change',
                         LinkCol('Aktivovat', 'device_status', url_kwargs=dict(item_id="id")))
    return render_template("public/devices/device-list.html", table=table, status=status)


@app.route("/device/add", methods=["GET", "POST"])
def device_add():
    # Stránka pro přidání záznamu
    form1 = AddDeviceForm(request.form)
    form1.location_id.query_factory = crud.get_form_locations
    form1.user_id.query_factory = crud.get_form_users

    if request.method == 'POST' and form1.validate():
        item = Device(name=form1.name.data, type=form1.type.data, ns=form1.ns.data,
                      location_id=form1.location_id.data.id, user_id=form1.user_id.data.id,
                      note=form1.note.data, status=True)
        crud.add_item(item=item)
        message = f"Záznam {item.name} byl úspěšně přidán"
        return render_template("public/devices/device-add.html", message=message)
    else:
        # upozornění po neúspěšné validaci formou <div class="alert alert-danger alert-dismissible">
        # for field, errors in form1.errors.items():
        #    for error in errors:
        #        flash("Chybné pole '{}': {}".format(
        #            getattr(form1, field).label.text,
        #            error
        #        ), 'error')
        return render_template("public/devices/device-add.html", form1=form1)


@app.route("/device/detail/<int:item_id>", methods=["GET", "POST"])
def device_detail(item_id):
    # Stránka pro editaci záznamu. Využívá stejný HTML vzor jako stránka pro přidání záznamu
    item = crud.get_item_by_id(model=Device, item_id=item_id)
    form1 = AddDeviceForm(obj=item)

    #    if item.status == True:
    #        form1.location_id.query = location_choice_active(get_id=item.location_id)
    #        form1.user_id.query = user_choice_active(get_id=item.user_id)
    #    else:

    # Formulář - zákaz prázdné hodnoty v rozbalovacím seznamu pro volbu lokace a uživatele
    form1.location_id.allow_blank = False
    form1.user_id.allow_blank = False

    # Formulář - naplnění rozbalovacího seznamů
    form1.location_id.query_factory = crud.get_form_locations
    form1.user_id.query_factory = crud.get_form_users

    # Formulář - předvolená hodnota seznamu = hodnota dle zobrazeného záznamu
    form1.location_id.data = crud.get_item_by_id(model=Location, item_id=item.location_id)
    form1.user_id.data = crud.get_item_by_id(model=User, item_id=item.user_id)

    form1.submit.label = text("Aktualizovat záznam")

    if request.method == 'POST' and form1.validate_on_submit():

        item.name = form1.name.data
        item.type = form1.type.data
        item.ns = form1.ns.data
        item.location_id = form1.location_id.raw_data[0]
        item.user_id = form1.user_id.raw_data[0]
        item.note = form1.note.data
        item.change_date = datetime.now()

        crud.update_item(item=item)
        message = f"Záznam {item.name} byl úspěšně aktualizován"
        # flash('Záznam byl úspěšně aktualizován', category="message")
        return render_template("public/devices/device-add.html", message=message, item_status=item.status)
    else:
        return render_template("public/devices/device-add.html", form1=form1)


# Stránka pro změnu stavu záznamu (aktivace / deaktivace)
@app.route("/device/status/<int:item_id>", methods=["GET", "POST"])
def device_status(item_id):
    item = crud.get_item_by_id(model=Device, item_id=item_id)
    filters = "active" if item.status else "inactive"

    if request.method == "POST":
        choice = request.form['choice']
        if choice == "change_status":
            item.change_date = datetime.now()
            item.status = not item.status

            crud.update_item(item=item)

            if item.status:
                flash('Záznam byl úspěšně aktivován', category="message")
            else:
                flash('Záznam byl úspěšně deaktivován', category="message")
        else:
            flash('Storno / neplatná volba', category="message")
        return redirect(url_for('device_list', filters=filters))

    elif request.method == "GET":
        return render_template(
            "public/devices/device-change-status.html", item=item)
