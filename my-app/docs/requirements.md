# Qonnect requirements

**Setting:** MSU-IIT Registrar and Cashier offices, weekday office hours during busy periods such as enrollment, payment deadlines and document requests

**People who wait:** MSU-IIT students who come to the Registrar or Cashier for enrollment, document requests, payments and fees, student records, registration or clearance verification. They are often on their phones between classes. See [Aira Villanueva](week3/personas.md#aira-villanueva-the-person-waiting) in docs/week3/personas.md.

**People who serve:** Registrar and Cashier counter staff who handle transactions on an office desktop and answer students' questions at the same time. See [Ramon Dela Cruz](week3/personas.md#ramon-dela-cruz-the-staff-member) in docs/week3/personas.md.


**Problem statement:** A student who visits the Registrar or Cashier between classes needs a way to get a queue ticket and see their position and status from their phone without standing in one long line, because right now they can't tell when their turn will come and risk missing class or a deadline while they wait.

## Functional requirements

★ = specific to the MSU-IIT Registrar and Cashier setting.

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue for a service by entering their name, 8-digit student ID and school email. | Must | **Yes** | Built (Week 3) |
| FR-02 ★ | A student must confirm that they have the documents the service requires before they can get a ticket. | Must | No | Built (Week 3) |
| FR-03 | A student can see their ticket number, service, status and how many people are ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-04 | A student's ticket page updates its status by itself every 10 seconds and shows the time of the last update. | Must | No | Built (Week 3) |
| FR-05 | A student can see an estimated wait time that is clearly labelled as an estimate. | Should | No | Built (Week 3) |
| FR-06 | A student can leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| FR-07 | A staff member can filter the queue to show one service only. | Must | No | Built (Week 3) |
| FR-08 | A staff member can call the earliest waiting ticket for a service. | Must | **Yes** | Built (Week 3) |
| FR-09 | A staff member can mark a called ticket as served or no-show. | Must | **Yes** | Built (Week 3) |
| FR-10 | A staff member must sign in before they can see the staff dashboard or change a ticket. | Must | **Yes** | Later |
| FR-11 | A staff member can add, rename and switch off a service, and a switched-off service no longer appears on the Join form. | Must | **Yes** | This week |
| FR-12 ★ | A student can read the plain-language instructions and required documents for a service before joining its queue. | Must | **Yes** | This week |
| FR-13 | A staff member can only mark a ticket served or no-show after it has been called. Waiting tickets show no Serve or No-show button. | Should | No | This week |
| FR-14 | A student can hold only one active ticket per service at a time, checked by student ID. | Should | **Yes** | Later |
| FR-15 ★ | A staff member can set the counter they are working at (for example "Registrar Window 2"), and a called student's ticket page shows which counter to go to. | Should | **Yes** | Later |
| FR-16 ★ | A staff member can set whether a service allows remote joining or in-person joining only, and the Join form follows that setting. | Should | **Yes** | Later |
| FR-17 | A staff member can see, for each service and day, how many tickets were served, marked no-show or left before being served. | Should | **Yes** | Later |
| FR-18 ★ | Each ticket number starts with a service prefix (for example D-012 for Document Requests) so students and staff can tell which line a ticket belongs to. | Could | **Yes** | Later |
| FR-19 ★ | A person with a disability or a pregnant student can join a priority lane that is called before the regular line. | Could | **Yes** | Later |
| FR-20 | A student can switch the page to a larger text size. | Could | No | Later |

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket, service or status change is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two students can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | When staff change a ticket's status, the student's ticket page shows the change within 10 seconds. | Performance | Must |
| NFR-04 | The My ticket page loads in under 2 seconds on a phone with mobile data. | Performance | Should |
| NFR-05 | A first-time student can join the queue from the home page in under 30 seconds on a phone. | Usability | Should |
| NFR-06 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-07 | Pages students can open never show another student's name, email or student ID. Only staff pages show them. | Privacy | Must |
| NFR-08 | No password or secret key is stored in the repository. | Security | Must |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-04, FR-06, FR-07, FR-08, FR-09, FR-10, FR-11, FR-12, NFR-01, NFR-02, NFR-03, NFR-06, NFR-07, NFR-08

This is the smallest version that still solves the problem. A student can find the right service, get a ticket, follow their place from their phone and leave if they need to. Staff can sign in, keep the service list correct, and move tickets through call, serve and no-show without losing any data. Without any one of these, students go back to standing in line or staff go back to tracking the queue by hand.

## Out of scope

- **SMS or email alerts when a ticket is called.** Texts cost money, and the university would need to approve sending email from its domain. The ticket page already updates itself every 10 seconds.
- **Paying fees inside the app.** Payments go through the Cashier and the university's own systems, and handling money safely is beyond this course.
- **Checking student IDs against the university's student records.** We don't have access to MSU-IIT's student information system, so the app only checks the ID's format.

## Checked with a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| 3rd-year student | "[their words]" | [e.g. Added FR-21 (Should) / Moved FR-15 to Must / Kept the list because …] |
