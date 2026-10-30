import os
import re

from datetime import timedelta, timezone
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Counter, Document, Service, ServiceDocument, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving

@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

def wait_estimate(ahead, avg_minutes):
    """Only an estimate: real transactions vary in length."""
    if ahead == 0:
        return f"under {avg_minutes} minutes"
    return f"about {ahead * avg_minutes} minutes"

def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)

@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html")

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return render_template("ticket.html", ticket=t, service=t.service, ahead=ahead,
                           wait_text=wait_estimate(ahead, t.service.avg_minutes))

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash(f"You left the queue. Ticket #{t['number']} has been cancelled.", "info")
    return redirect(url_for("index"))


def all_services():
    # FR-11: a switched-off service no longer appears on the Join form
    return db.session.scalars(
        db.select(Service).filter_by(is_active=True).order_by(Service.name)
    ).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    student_id = form.get("student_id", "").strip()
    has_documents = form.get("has_documents") == "on"
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 100:
        errors["name"] = "Enter your name (up to 100 characters)."
    # Same pattern as ck_users_email_format, so the database never rejects it
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None or not service.is_active:
        errors["service_id"] = "Choose a service."
    match = re.fullmatch(r"(\d{4})-?(\d{4})", student_id)
    if match is None:
        errors["student_id"] = "Enter your 8-digit student ID, for example 2024-0013."
    else:
        # Store as 2024-0013 to match ck_users_student_id_format
        student_id = f"{match[1]}-{match[2]}"
    if not has_documents:
        errors["has_documents"] = "Confirm you have the required documents before joining."

    user = None
    if not errors:
        user = db.session.scalar(db.select(User).filter_by(student_id=student_id))
        if user is None:
            if db.session.scalar(db.select(User).filter_by(email=email)) is not None:
                errors["email"] = "This email is already used with a different student ID."
        elif user.email != email:
            errors["student_id"] = "This student ID is registered with a different email."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    if user is None:
        user = User(name=name, email=email, student_id=student_id)
    else:
        # FR-14: one active ticket per student per service
        active = db.session.scalar(
            db.select(Ticket).filter(Ticket.user_id == user.id,
                                     Ticket.service_id == service.id,
                                     Ticket.status.in_(("waiting", "called")))
        )
        if active is not None:
            flash(f"You are already in this queue. Your ticket is #{active.id}.", "info")
            return redirect(url_for("ticket", ticket_id=active.id))

    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    return render_template("staff.html", queue=queue, services=all_services(),
                           selected=service_id)

@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)
    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return {"status": t.status, "ahead": ahead,
            "wait_text": wait_estimate(ahead, t.service.avg_minutes)}

@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Enrollment", "E", 5),
        ("Document Requests", "D", 5),
        ("Payments and Fees", "P", 5),
        ("Student Records", "S", 5),
        ("Registration", "R", 5),
        ("Clearance Verification", "C", 5),
    ]
    for name, prefix, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, prefix=prefix, avg_minutes=minutes))
    db.session.commit()
    print("Services are ready.")

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
