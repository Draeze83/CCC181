# Qonnect

Qonnect is a web app for queueing at the **MSU-IIT Registrar and Cashier offices**. Students choose a service, get a queue ticket on their phone or laptop, and see how many people are ahead of them without standing in line. Office staff use a dashboard to call the next ticket and mark tickets as served or no-show.

Built with Python, Flask and Bootstrap 5 for **CCC181**.

## Setting

| | |
| --- | --- |
| **Where** | MSU-IIT Registrar and Cashier offices |
| **Who waits** | Students, mostly using a phone browser between classes |
| **Who serves** | Office staff at a service counter, using a desktop computer |
| **Services** | Enrollment, Document Requests, Payments and Fees, Student Records, Registration, Clearance Verification |

## Pages

| URL | Page | Who uses it |
| --- | --- | --- |
| `/` | Home | Students |
| `/join` | Join the queue: choose a service and get a ticket | Students |
| `/queue/<ticket_id>` | My ticket: number, status, people ahead, estimated wait (refreshes every 10 seconds) | Students |
| `/staff` | Staff dashboard: filter by service, call next, mark served or no-show | Staff |

## How to run it

You need [Python 3](https://www.python.org/downloads/) and Git.

**1. Get the code**

```bash
git clone https://github.com/Draeze83/Qonnect-Python-Flask-App-.git
cd Qonnect-Python-Flask-App-
```

**2. Create and activate a virtual environment** (create it once; activate it in every new terminal)

```bash
python -m venv .venv

.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux
```

Your prompt shows `(.venv)` when it is active. If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

**3. Install the packages**

```bash
pip install -r my-app/requirements.txt
```

**4. Start the app from inside the `my-app` folder**

```bash
cd my-app
flask --app app run --debug
```

**5. Open http://127.0.0.1:5000 in your browser.**

## Things to know

- **Run it from `my-app`.** If you see `Error: Could not import 'app'`, you are in the wrong folder. `cd my-app` and try again.
- **Tickets reset when the server restarts.** Tickets are kept in memory for now, so saving `app.py` (which restarts the server in debug mode) brings back the four sample tickets. A ticket page you had open will then show "Not Found". Get a new ticket from `/join`. Tickets move to a database in Week 4.
- **Debug mode is for development only.** Do not use `--debug` on a public server.

## Project structure

```
my-app/
├── app.py              # routes, sample tickets and services
├── requirements.txt    # Python packages
├── templates/          # Jinja2 pages
│   ├── base.html       # shared layout and navigation
│   ├── index.html      # home page
│   ├── join.html       # join-the-queue form
│   ├── ticket.html     # My ticket page
│   └── staff.html      # staff dashboard
├── static/
│   ├── css/style.css
│   └── js/main.js
└── docs/               # proposal, personas, wireframes, report
```
