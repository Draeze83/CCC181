"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

# Sample data for the demo. A real app would load this from a database later.
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
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
