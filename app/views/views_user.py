from datetime import date
from flask import request, render_template, flash, url_for, redirect
from sqlalchemy import text

from app import app
from app.views.tables import UserTable, LinkCol
from app.views.forms import AddUserForm
from app.db.models import User
from app.db import crud


@app.route("/user/?filters=<filters>")
@app.route("/user/")
def user_list(filters="active"):
    # Stránka se seznamem záznamů
    status = False if filters == "inactive" else True
    users = crud.get_items_status(model=User, status=status)
    table = UserTable(users)
    if status:
        table.add_column('status_change', LinkCol('Deaktivovat', 'user_change_status', url_kwargs=dict(item_id='id')))
    else:
        table.add_column('status_change', LinkCol('Aktivovat', 'user_change_status', url_kwargs=dict(item_id='id')))
    return render_template("public/users/user-list.html", table=table, status=status)


@app.route("/user/add", methods=["GET", "POST"])
def user_add():
    # Stránka pro přidání záznamu
    form1 = AddUserForm(request.form)

    if request.method == 'POST' and form1.validate():
        item = User(name=form1.name.data, email=form1.email.data, status=True)
        crud.add_item(item=item)
        message = f"Záznam {item.name} byl úspěšně přidán"
        return render_template("public/users/user-add.html", message=message)
    else:
        return render_template("public/users/user-add.html", form1=form1)


# Stránka pro editaci záznamu. Využívá stejný HTML vzor jako stránka pro přidání záznamu
@app.route("/user/detail/<int:item_id>", methods=["GET", "POST"])
def user_detail(item_id):
    item = crud.get_item_by_id(model=User, item_id=item_id)

    form1 = AddUserForm(obj=item)
    form1.submit.label = text("Aktualizovat záznam")

    if request.method == 'POST' and form1.validate_on_submit():
        item.name = form1.name.data
        item.email = form1.email.data
        item.change_date = date.today()

        crud.update_item(item=item)
        message = f"Záznam {item.name} byl úspěšně aktualizován"
        return render_template("public/users/user-add.html", message=message, item_status=item.status)
    else:
        return render_template("public/users/user-add.html", form1=form1)


# Stránka pro změnu stavu záznamu (aktivace / deaktivace)
@app.route("/user/status/<int:item_id>", methods=["GET", "POST"])
def user_change_status(item_id):
    item = crud.get_item_by_id(model=User, item_id=item_id)
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
        return redirect(url_for('user_list', filters=filters))

    elif request.method == "GET":
        return render_template(
            "public/users/user-change-status.html", item_id=item_id, item=item
        )
