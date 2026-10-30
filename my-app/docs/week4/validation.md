# Validation in three layers

| Rule | Layer | How I tested it | What happened |
|---|---|---|---|
| Required fields, email format, max length | Browser | Submitted the Join form empty, typed `abc` as email, typed 101+ characters as name | Browser blocked the submit and stopped typing at the limit |
| Email must be valid, name required, service must exist | Flask | curl with `name=`, `email=not-an-email`, `service_id=999` | 400 BAD REQUEST, nothing saved |
| Name is at most 100 characters | Flask | curl with a 200-character name, other fields valid | 400 BAD REQUEST, nothing saved |
| Student ID must be `0000-0000` | Flask | curl with `student_id=abc`, other fields valid | 400 BAD REQUEST, nothing saved |
| Service must be active | Flask | Switched Registration off, then curl with `service_id=5` | 400 BAD REQUEST, nothing saved |
| Service must exist | Database (FOREIGN KEY) | `INSERT INTO tickets (user_id, service_id) VALUES (3, 999);` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Status must be an allowed value | Database (CHECK) | `UPDATE tickets SET status = 'lost', called_at = now() WHERE id = 3;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Average minutes must be above 0 | Database (CHECK) | `INSERT INTO services (name, prefix, avg_minutes) VALUES ('Test', 'T', 0);` | `ERROR: new row for relation "services" violates check constraint "ck_services_avg_minutes"` |
| Email must be unique | Database (UNIQUE) | `INSERT INTO users (name, email, student_id) VALUES ('Copy', 'ana@school.edu', '2024-9999');` | `ERROR: duplicate key value violates unique constraint "users_email_key"` |
| One active ticket per student per service | Database (UNIQUE, partial index) | `INSERT INTO tickets (user_id, service_id) VALUES (3, 5);` | `ERROR: duplicate key value violates unique constraint "uq_tickets_one_active"` |
| Service prefix is required | Database (NOT NULL) | `INSERT INTO services (name, avg_minutes) VALUES ('Test', 5);` | `ERROR: null value in column "prefix" of relation "services" violates not-null constraint` |
| A service with tickets cannot be deleted | Database (ON DELETE RESTRICT) | `DELETE FROM services WHERE id = 5;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
| Database fills in defaults | Database | `INSERT INTO tickets (user_id, service_id) VALUES (3, 1) RETURNING id, status, created_at;` | Row saved as ticket 6 with `status = waiting` and `created_at = 2026-10-30 01:45:58+00` |

## No SQL in f-strings
`git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"` printed nothing.
