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

You need [Python 3](https://www.python.org/downloads/), Git, and [Docker Desktop](https://www.docker.com/products/docker-desktop/) (it runs the PostgreSQL database). Start Docker Desktop before step 3.

**1. Get the code and go into the `my-app` folder**

```bash
git clone https://github.com/Draeze83/Qonnect-Python-Flask-App-.git
cd Qonnect-Python-Flask-App-/my-app
```

Run every command below from inside `my-app`.

**2. Create your `.env` file from the example**

```bash
cp .env.example .env            # macOS/Linux, Git Bash, or PowerShell
copy .env.example .env          # Windows Command Prompt
```

`.env` holds the database password and connection URL. It is ignored by Git, so it never gets committed. You can keep `change-me` for local work; if you change it, change it in both lines.

**3. Start the database**

```bash
docker compose up -d
```

This starts PostgreSQL 17 in a container named `qonnect-db` on port 5432. Check it with `docker compose ps`; wait until it shows `healthy`.

**4. Create and activate a virtual environment** (create it once; activate it in every new terminal)

```bash
python -m venv .venv

.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux
```

Your prompt shows `(.venv)` when it is active. If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

**5. Install the packages**

```bash
pip install -r requirements.txt
```

**6. Create the tables**

```bash
flask --app app db upgrade
```

This runs the migrations in `migrations/` against the database.

**7. Add the starting services**

```bash
flask --app app seed
```

It prints `Services are ready.` Running it again is safe; it skips services that already exist.

**8. Start the app**

```bash
flask --app app run --debug
```

**9. Open http://127.0.0.1:5000 in your browser.**

Next time, you only need to start Docker Desktop, then run `docker compose up -d`, activate the virtual environment, and `flask --app app run --debug`. To stop the database, run `docker compose down` (your data is kept in the `pgdata` volume).

## Things to know

- **Run it from `my-app`.** If you see `Error: Could not import 'app'`, you are in the wrong folder. `cd my-app` and try again.
- **The database must be running.** If the app fails with `connection refused` or `could not connect to server`, Docker Desktop is closed or the container is stopped. Start Docker Desktop and run `docker compose up -d`.
- **`KeyError: 'DATABASE_URL'` means `.env` is missing.** Copy `.env.example` to `.env` (step 2).
- **Debug mode is for development only.** Do not use `--debug` on a public server.

## Project structure

```
Qonnect-Python-Flask-App-/
└── my-app/
    ├── app.py                      # Flask app: routes, sample tickets and services
    ├── requirements.txt            # Python packages to install
    ├── README.md                   # this file
    ├── .gitignore                  # keeps .venv and caches out of Git
    ├── templates/                  # Jinja2 pages
    │   ├── base.html               # shared layout, navigation bar and footer
    │   ├── index.html              # home page
    │   ├── join.html               # join-the-queue form
    │   ├── ticket.html             # My ticket page (auto-refreshing status)
    │   └── staff.html              # staff dashboard
    ├── static/
    │   ├── css/
    │   │   └── style.css           # custom styles
    │   └── js/
    │       └── main.js             # form focus and submit behavior
    └── docs/
        ├── week1/
        │   └── proposal.txt        # project proposal
        └── week3/
            ├── report.md           # Week 3 report
            ├── personas.md         # student and staff personas
            ├── feedback.md         # wireframe self-review
            ├── accessibility.md    # Lighthouse and keyboard checks
            ├── usability-test.md   # usability test notes
            ├── wireframes/
            │   ├── wireframes_before.png    # first wireframes
            │   ├── wireframes-revised.png   # revised wireframe sheet
            │   ├── join-phone.png
            │   ├── join-laptop.png
            │   ├── ticket-phone.png
            │   ├── ticket-laptop.png
            │   ├── staff-phone.png
            │   └── staff-laptop.png
            └── screenshots/
                ├── aira-villanueva.jpg        # persona image
                ├── ramon-dela-cruz.jpg        # persona image
                ├── join-phone.png             # app screenshots, phone and laptop
                ├── join-laptop.png
                ├── ticket-phone.png
                ├── ticket-laptop.png
                ├── staff-phone.png
                ├── staff-laptop.png
                ├── join-demo.jpg              # demo photos
                ├── join-form-demo.jpg
                ├── my-ticket-demo.jpg
                ├── staff-dashboard-demo.jpg
                ├── homepage.png               # Lighthouse results
                ├── join_form.png
                ├── ticket.png
                └── staff-dashboard.png
```