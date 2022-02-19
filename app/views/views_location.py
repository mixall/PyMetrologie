from datetime import date
from flask import request, render_template, flash, url_for, redirect
from sqlalchemy import text

from app import app
from app.views.tables import LocationTable, LinkCol
from app.views.forms import AddLocationForm
from app.db.models import Location
from app.db import crud


@app.route("/location/?filters=<filters>")
@app.route("/location/")
def location_list(filters="active"):
    # Stránka se seznamem záznamů
    status = False if filters == "inactive" else True
    locations = crud.get_items_status(model=Location, status=status)
    table = LocationTable(locations)
    if status:
        table.add_column('status_change',
                         LinkCol('Deaktivovat', 'location_change_status', url_kwargs=dict(item_id='id')))
    else:
        table.add_column('status_change',
                         LinkCol('Aktivovat', 'location_change_status', url_kwargs=dict(item_id='id')))
    return render_template("public/locations/location-list.html", table=table, status=status)


@app.route("/location/add", methods=["GET", "POST"])
def location_add():
    # Stránka pro přidání záznamu
    form1 = AddLocationForm(request.form)

    if request.method == 'POST' and form1.validate():
        item = Location(name=form1.name.data, address=form1.address.data, status=True)

        crud.add_item(item=item)
        message = f"Záznam {item.name} byl úspěšně přidán"
        return render_template("public/locations/location-add.html", message=message)
    else:
        return render_template("public/locations/location-add.html", form1=form1)


@app.route("/location/detail/<int:item_id>", methods=["GET", "POST"])
def location_detail(item_id):
    # Stránka pro editaci záznamu. Využívá stejný HTML vzor jako stránka pro přidání záznamu
    item = crud.get_item_by_id(model=Location, item_id=item_id)
    form1 = AddLocationForm(obj=item)

    form1.submit.label = text("Aktualizovat záznam")

    if request.method == 'POST' and form1.validate_on_submit():
        item.name = form1.name.data
        item.address = form1.address.data
        item.change_date = date.today()

        crud.update_item(item=item)
        message = f"Záznam {item.name} byl úspěšně aktualizován"
        return render_template("public/locations/location-add.html", message=message, item_status=item.status)
    else:
        return render_template("public/locations/location-add.html", form1=form1)


@app.route("/location/status/<int:item_id>", methods=["GET", "POST"])
def location_change_status(item_id):
    # Stránka pro změnu stavu záznamu (aktivace / deaktivace)
    item = crud.get_item_by_id(model=Location, item_id=item_id)
    filters = "active" if item.status else "inactive"

    if request.method == "POST":
        choice = request.form['choice']
        if choice == "change_status":
            item.change_date = date.today()
            item.status = not item.status
            crud.update_item(item=item)
            if item.status:
                flash('Záznam byl úspěšně aktivován', category="message")
            else:
                flash('Záznam byl úspěšně deaktivován', category="message")
        else:
            flash('Storno / neplatná volba', category="message")
        return redirect(url_for('location_list', filters=filters))

    elif request.method == "GET":
        return render_template(
            "public/locations/location-change-status.html", item=item)
