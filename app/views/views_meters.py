from datetime import datetime
from flask import request, render_template, flash, url_for, redirect
from sqlalchemy import text

from app import app
from app.views.tables import MeterTable, LinkCol
from app.views.forms import AddMeterForm
from app.db.models import Meter, Device
from app.db import crud


@app.route("/meter/?filters=<filters>")
@app.route("/meter/")
def meter_list(filters="active"):
    # Stránka se seznamem záznamů
    status = False if filters == "inactive" else True
    meters = crud.get_items_status(model=Meter, status=status)
    table = MeterTable(meters)
    if status:
        table.add_column('status_change',
                         LinkCol('Deaktivovat', 'meter_status', url_kwargs=dict(item_id="id")))
    else:
        table.add_column('status_change',
                         LinkCol('Aktivovat', 'meter_status', url_kwargs=dict(item_id="id")))
    return render_template("public/meters/meter-list.html", table=table, status=status)


@app.route("/meter/add", methods=["GET", "POST"])
def meter_add():
    # Stránka pro přidání záznamu
    form1 = AddMeterForm(request.form)
    form1.act_dev_id.query_factory = crud.get_form_devices
    form1.home_dev_id.query_factory = crud.get_form_devices

    if request.method == 'POST' and form1.validate():
        item = Meter(name=form1.name.data, model=form1.model.data, act_dev_id=form1.act_dev_id.data.id,
                     act_dev_detail=form1.act_dev_detail.data, home_dev_status=form1.home_dev_status.data,
                     home_dev_id=form1.home_dev(), status=True)
        crud.add_item(item=item)
        message = f"Záznam {item.name} byl úspěšně přidán"
        return render_template("public/meters/meter-add.html", message=message)
    else:
        return render_template("public/meters/meter-add.html", form1=form1)


@app.route("/meter/detail/<int:item_id>", methods=["GET", "POST"])
def meter_detail(item_id):
    # Stránka pro editaci záznamu. Využívá stejný HTML vzor jako stránka pro přidání záznamu
    item = app.session.query(Meter).filter(Meter.id == item_id).first()
    form1 = AddMeterForm(obj=item)

    # Formulář - zákaz prázdné hodnoty v rozbalovacím seznamu pro volbu aktuálnního zařízení
    form1.act_dev_id.allow_blank = False

    # Formulář - naplnění rozbalovacích seznamů
    form1.act_dev_id.query_factory = crud.get_form_devices
    form1.home_dev_id.query_factory = crud.get_form_devices

    # Formulář - předvolená hodnota seznamu = hodnota dle zobrazeného záznamu
    form1.act_dev_id.data = crud.get_item_by_id(model=Device, item_id=item.act_dev_id)
    form1.home_dev_id.data = crud.get_item_by_id(model=Device, item_id=item.home_dev_id)

    form1.submit.label = text("Aktualizovat záznam")

    if request.method == 'POST' and form1.validate_on_submit():

        item.name = form1.name.data
        item.model = form1.model.data
        item.act_dev_id = form1.act_dev_id.raw_data[0]
        item.act_dev_detail = form1.act_dev_detail.data
        item.home_dev_status = form1.home_dev_status.data
        if item.home_dev_status:
            item.home_dev_id = form1.home_dev_id.raw_data[0]
        else:
            item.home_dev_id = form1.act_dev_id.raw_data[0]
        item.change_date = datetime.now()

        app.session.commit()
        message = f"Záznam {item.name} byl úspěšně aktualizován"
        flash('Záznam byl úspěšně aktualizován', category="message")
        return render_template("public/meters/meter-add.html", message=message, item_status=item.status)
    else:
        return render_template("public/meters/meter-add.html", form1=form1)


# Stránka pro změnu stavu záznamu (aktivace / deaktivace)
@app.route("/meter/status/<int:item_id>", methods=["GET", "POST"])
def meter_status(item_id):
    item = app.session.query(Meter).filter(Meter.id == item_id).first()
    filters = "active" if item.status == True else "inactive"
    if request.method == "POST":
        choice = request.form['choice']
        if choice == "change_status":
            item.change_date = datetime.now()
            item.status = not item.status
            app.session.commit()
            if item.status:
                flash('Záznam byl úspěšně aktivován', category="message")
            else:
                flash('Záznam byl úspěšně deaktivován', category="message")
        else:
            flash('Storno / neplatná volba', category="message")
        return redirect(url_for('meter_list', filters=filters))

    elif request.method == "GET":
        return render_template(
            "public/meters/meter-change-status.html", item=item)
