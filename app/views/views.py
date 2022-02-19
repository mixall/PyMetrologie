from app import app
from flask import render_template


@app.route("/")
def index():
    return render_template("public/index.html")


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('public/error.html', pagetitle="404 Error - Page Not Found",
                           pageheading="Page not found (Error 404)", error=e), 404


@app.errorhandler(405)
def form_not_posted(e):
    return render_template('public/error.html', pagetitle="405 Error - Form Not Submitted",
                           pageheading="The form was not submitted (Error 405)", error=e), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('public/error.html', pagetitle="500 Error - Internal Server Error",
                           pageheading="Internal server error (500)", error=e), 500
