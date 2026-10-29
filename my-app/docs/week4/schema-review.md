# Schema self-review

## Part 1: Answers to the six questions

### 1. Coverage

**Does every requirement marked Stores data? = Yes have a table or column?**
Yes. Fourteen requirements were marked Yes: FR-01, FR-03, FR-06, FR-08, FR-09, FR-10, FR-11, FR-12, FR-14, FR-15, FR-16, FR-17, FR-18 and FR-19, and Entry 3 adds FR-05, making fifteen. Each has a row in 2a of `schema.md`.

**Does each persona's top task from Week 3 have the data it needs?**
Yes.
- **Aira's tasks:** FR-12 (find a service and read its instructions) uses `services.name`, `services.is_active`, `services.instructions` and the document tables. FR-01 (get a ticket) uses `users` and `tickets`, while FR-03 (see her ticket number, service, status and people ahead) uses `tickets.id` + `services.prefix`, `tickets.service_id` → `services.name` and `tickets.status`, and the position is computed.
- **Ramon's tasks:** FR-10 (sign in) uses `users.role` and `users.password_hash`. FR-08 (call the earliest eligible ticket) uses `tickets.service_id`, `status`, `is_priority` and `created_at`. FR-09 (valid status change) uses `tickets.status`, `called_at` and `finished_at`. His need to see his counter uses `users.counter_id`.

**Is there any table or column that no requirement needs?**
Yes, three columns:
- `services.avg_minutes` is used by the wait estimate (FR-05), but FR-05 is marked Stores data? = No in `requirements.md`. The column is needed; the requirement was marked wrongly.
- `service_documents.copies` is not mentioned in FR-12.
- `users.created_at` is not needed by any requirement.

### 2. One fact in one place

**Is any fact stored in more than one row or table?**
Mostly no. Each fact has one home, and other tables refer to it by key:
- A person's name, email and student ID are only in `users`. `tickets` stores `user_id` only.
- A service's name, prefix, instructions, average minutes and on/off setting are only in `services`.
- A counter's name is only in `counters`, and a document's name is only in `documents`.
- `users.counter_id` (where a staff member works now) and `tickets.counter_id` (where this ticket was called) are different facts, so neither is a copy of the other.

**One problem found:** whether a ticket is finished is stored twice, in `tickets.status` ('served', 'no-show', 'left') and in `tickets.finished_at`. Nothing forces them to agree. I kept both, because status says *what happened* and the timestamp says *when*, and added a CHECK that ties them together. See Entry 2.

### 3. Facts, not results

**Am I storing anything I could compute instead?**
No. Everything I store is a fact that was entered or recorded, and everything that depends on the current state of the queue is computed when needed:

| Computed, not stored | Computed from |
| --- | --- |
| Position in line and people ahead | `tickets.service_id`, `status`, `is_priority`, `created_at` |
| Estimated wait | people ahead × `services.avg_minutes` |
| Ticket number such as D-012 | `services.prefix` + `tickets.id` |
| Daily served / no-show / left counts (FR-17) | COUNT of `tickets` grouped by service, day and `status` |
| Last-updated time on the ticket page | the time of the last refresh |

Two stored columns could look like results, but are not:
- `services.avg_minutes` is a setting that staff choose. It is the starting estimate until there is enough ticket history to average.
- `tickets.status` is not derivable from the timestamps, because "served", "no-show" and "left" cannot be told apart from `called_at` and `finished_at` alone.

One computed value has a limit: the ticket number uses `tickets.id`, which is one sequence shared by all services and never reset. Document Requests tickets could be D-001, D-004, D-009, and numbers keep growing day after day (D-4512). I accept this for now because it still guarantees that no two students get the same number (NFR-02).

### 4. Bad data

I went through the mistakes the personas could make and named the constraint that stops each.

| Mistake | What stops it |
| --- | --- |
| Aira double-taps Join | The partial UNIQUE index on `tickets (user_id, service_id) WHERE status IN ('waiting', 'called')` allows only one active ticket per student per service. UNIQUE on `users.email` and `users.student_id` stops a duplicate account being created by the same double tap. |
| Typo in the student ID | `CHECK (student_id ~ '^[0-9]{4}-[0-9]{4}$')` rejects the wrong format. The current app accepts the ID without a dash, so the app must put the dash back before saving. A typo in the right format (2024-0031 for 2024-0013) cannot be caught, because the app does not check IDs against the student records (see Out of scope in `requirements.md`). |
| Typo in the email | **Partly Stopped.** After Entry 1, two CHECKs reject a badly formed or uppercase email. A typo in a well-formed address (`aira@msuiit.edu.hp`) still cannot be caught. |
| Picking a service that does not exist | The foreign key on `tickets.service_id`. |
| Picking a service that is switched off | **Not stopped by a constraint.** A CHECK or foreign key cannot look at another row's `is_active`. A trigger could, but I chose to keep the rule in the app: it must only accept services where `is_active = true`. See Entry 4. |
| Ramon marks a waiting ticket as served | `CHECK (status IN ('waiting', 'left') OR called_at IS NOT NULL)` rejects a served or no-show ticket that was never called. |
| An invalid status, role or prefix | CHECKs on `status`, `role` and `prefix`. |
| A staff account with no password, or a student with no ID | The two table rules on `users`. |
| Zero or negative minutes or copies | `CHECK (avg_minutes > 0)` and `CHECK (copies > 0)`. |
| A ticket finished before it was created or called | `CHECK (called_at >= created_at)`, `CHECK (finished_at >= created_at)`, and, after Entry 2, `CHECK (finished_at >= called_at)`. |
| A ticket that is finished according to one column but not the other | The CHECK added in Entry 2. |
| The same document listed twice for one service | The composite PRIMARY KEY on `service_documents`. |
| Two services with the same name or prefix | UNIQUE on `services.name` and `services.prefix`. |
| A student given a counter | **Not stopped yet.** Nothing enforces that `users.counter_id` is empty for students. `CHECK (role = 'staff' OR counter_id IS NULL)` would stop it. Will be worked later. |
| A called ticket with no counter | **Not stopped.** A called, served or no-show ticket can have no `counter_id`, so the ticket page (FR-15) could show no counter. The app must set the counter when it calls a ticket. |
| A waiting ticket with a call time | **Not stopped yet.** `CHECK (status <> 'waiting' OR called_at IS NULL)` would stop it. Will be worked later. |
Two kinds of mistake are not covered by a database constraint, so the app must handle them: two staff members calling the same ticket at once, and a ticket moving backwards (for example 'served' to 'called'). The app will change a status only with `UPDATE ... WHERE status = 'waiting'` (or the status it expects), so the second change updates nothing.

### 5. Deletes

**Did I choose RESTRICT, CASCADE or SET NULL on purpose for every foreign key?**
Yes. Each rule is in the delete-rules table in 2d of `schema.md`, with its reason.

| Foreign key | Rule | Could it destroy history that staff need? |
| --- | --- | --- |
| `tickets.user_id` → users | RESTRICT | No. A student with tickets cannot be deleted, so old tickets stay for reports. |
| `tickets.service_id` → services | RESTRICT | No. A service with tickets cannot be deleted; staff switch it off with `is_active` instead. |
| `tickets.counter_id` → counters | RESTRICT | No. A counter that has called a ticket cannot be deleted. |
| `users.counter_id` → counters | SET NULL | No. Only the staff member's current assignment is cleared. The person stays, and tickets keep their own `counter_id`. |
| `service_documents.service_id` → services | CASCADE | No. A service that ever had a ticket cannot be deleted at all because of the RESTRICT above, so CASCADE only removes the document links of a service that never had a ticket. |
| `service_documents.document_id` → documents | RESTRICT | No. A document still used by a service cannot be deleted. |

No delete can remove a ticket, because no rule cascades to `tickets`. The cost of RESTRICT is that a student with tickets, or a counter that has called tickets, can never be deleted. I accepted this because the daily reports (FR-17) need the history, and no requirement asks for deleting people or counters.

### 6. Types

**Is every moment in time a `timestamptz`?**
Yes. The moments are `tickets.created_at`, `tickets.called_at` and `tickets.finished_at`, and all are `timestamptz`. (`users.created_at` was also `timestamptz` before Entry 3 removed it.) No date or time is stored as text. The daily report (FR-17) groups tickets by day, so the query must convert to the office's time zone first, for example `created_at AT TIME ZONE 'Asia/Manila'`. Otherwise, if the database session runs in UTC, a day would start at 8 a.m. Manila time instead of midnight.

**Is anything stored as text that should be a number, a date or a true/false value?**
No.
- Numbers (`avg_minutes`, `copies`, and all ids) are `integer`.
- Yes/no facts (`is_priority`, `allows_remote`, `is_active`) are `boolean`, not 'yes'/'no' text.
- `student_id` is text on purpose, because it is an identifier with a dash and leading zeros (2024-0013), not a number anyone does math on.
- `status` and `role` are `varchar` limited by a CHECK to a fixed set of words.
- `name`, `email`, `prefix`, `instructions` and `password_hash` are real text.

## Part 2: Entries

### Entry 1: email checks

**Works well:** Nothing a student sees on screen is stored as a result. Position in line, people ahead, estimated wait, the ticket number shown as D-012, and the daily served, no-show and left counts are all computed from `tickets.id`, `service_id`, `status`, `created_at`, `is_priority`, `services.prefix` and `services.avg_minutes`. A person leaving or joining never forces a rewrite of other rows (Question 3).

**Problem:** `users.email` only has NOT NULL and UNIQUE. Aira could type `aira@` or `aira@msuiit`, and the database would accept it. `Aira@msuiit.edu.ph` and `aira@msuiit.edu.ph` would also count as two different accounts, because UNIQUE is case-sensitive.

**Change:** Added two CHECK constraints to `users` in `schema.md` (2c): `CHECK (email = lower(email))` and `CHECK (email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$')`. The app already lowercases the email before saving, so the first CHECK matches what it does. The ERD does not change, because these are constraints and not columns.

### Entry 2: status and finished_at can disagree

**Works well:** The partial unique index on `tickets (user_id, service_id) WHERE status IN ('waiting', 'called')` stops a double tap on Join from creating two tickets for the same student and service. The `student_id` CHECK and UNIQUE also stop a badly formatted or duplicated student ID (Question 4).

**Problem:** Whether a ticket is finished is stored twice: once in `status` ('served', 'no-show', 'left') and once in `finished_at`. Nothing forces them to agree, so a ticket could be 'waiting' with a `finished_at`, or 'served' with none. That would break the FR-17 daily counts. Nothing checks that `finished_at` comes after `called_at` either. Question 2 found it (a fact in more than one place).

**Change:** Added two table rules to `tickets` in `schema.md` (2c): `CHECK ((status IN ('served', 'no-show', 'left')) = (finished_at IS NOT NULL))` and `CHECK (finished_at >= called_at)`. I kept both `status` and `finished_at` because they answer different questions: the status says what happened, and the timestamp says when. The ERD does not change.

### Entry 3: columns that no requirement needs

**Works well:** Every moment in time is `timestamptz` (`created_at`, `called_at`, `finished_at`). Numbers are `integer`, flags are `boolean`, and `student_id` is text on purpose because it is an ID with a dash and leading zeros, not a number (Question 6).

**Problem:** Three columns have no matching requirement (Question 1). `services.avg_minutes` is needed by FR-05, but `requirements.md` marks FR-05 as Stores data? = No. `service_documents.copies` is not mentioned in FR-12. `users.created_at` is not needed by any requirement.

**Change:**
- Changed FR-05 to Stores data? = **Yes** in `requirements.md`, because the wait estimate depends on a stored `avg_minutes`.
- Kept `copies`, and reworded FR-12 to "...instructions and required documents, and how many copies of each, ...". This supports Aira's goal of not making another trip because a requirement is missing, and it is the extra column that depends on both keys in the 2NF answer.
- Removed `users.created_at` from `users` in 2b, 2c and the ERD, since no requirement needs it. Tickets keep their own `created_at`, so the queue order and the `timestamptz` requirement are unaffected.

### Entry 4: a switched-off service can still receive a ticket

**Works well:** Every delete rule was chosen on purpose. `tickets.user_id`, `tickets.service_id` and `tickets.counter_id` are RESTRICT, so a delete can never erase the tickets that the FR-17 daily report counts. Staff retire a service by switching it off with `is_active`, not by deleting it. `users.counter_id` is SET NULL, because a staff member should survive a counter being removed (Question 5).

**Problem:** The foreign key on `tickets.service_id` checks that the service exists, but not that it is switched on. A student could still get a ticket for a service with `is_active = false`, for example from an old Join page left open. A CHECK constraint cannot look at another table, so no constraint can stop it. A trigger could, but I chose to keep the rule in the app.

**Change:** No change to the ERD or `schema.md`. A trigger could reject the insert, but I kept the rule in the app because it is one check in one place, and the app already checks the rest of the Join form. The app will:
- list only services where `is_active = true` on the Join form (FR-11)
- check again on submit with `INSERT INTO tickets ... SELECT ... FROM services WHERE id = :service_id AND is_active = true`, so a Join page left open after a service is switched off inserts nothing and shows "This service is closed."
- check `allows_remote` the same way for remote joins (FR-16). The database cannot check this, because a ticket does not record whether it was a remote join.