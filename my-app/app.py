"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""

import re
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

TICKETS = [
    {"number": 1, "name": "Kurt", "email": "kurt@school.edu", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Raven", "email": "raven@school.edu", "service_id": 2, "status": "waiting"},
    {"number": 3, "name": "Winchester", "email": "winchester@school.edu", "service_id": 3, "status": "waiting"},
    {"number": 4, "name": "James", "email": "james@school.edu", "service_id": 4, "status": "waiting"}
]

SERVICES = [
    {"id": 1, "name": "Enrollment"},
    {"id": 2, "name": "Document Requests"},
    {"id": 3, "name": "Payments and Fees"},
    {"id": 4, "name": "Student Records"},
    {"id": 5, "name": "Registration"},
    {"id": 6, "name": "Clearance Verification"}
]

@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html")

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash(f"You left the queue. Ticket #{t['number']} has been cancelled.", "info")
    return redirect(url_for("index"))


@app.route("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})

@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    student_id = form.get("student_id", "").strip()
    has_documents = form.get("has_documents") == "on"


    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    if not re.fullmatch(r"\d{4}-?\d{4}", student_id):
        errors["student_id"] = "Enter your 8-digit student ID, for example 2024-0013."
    if not has_documents:
        errors["has_documents"] = "Confirm you have the required documents before joining."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting",
                    "student_id": student_id})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES,
                           names=names, selected=service_id)

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
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}

@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
