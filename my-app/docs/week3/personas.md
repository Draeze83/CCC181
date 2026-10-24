## Aira Villanueva, the person waiting

> "Dugay kaayo ang linya sa cashier. Wala ko kabalo kung kanus-a pa akoang turn."

| | |
| --- | --- |
| **Photo or sketch** | [A drawing, an icon, or a free stock photo. Never a photo of the real person you interviewed.] |
| **Age, role and background** | 20, 2nd-year MSU-IIT student. She balances academic requirements with classes and needs to visit university offices for student services. |
| **Goals** | 1. Complete the correct registrar or cashier transaction in one visit. 2. Know her queue position and when she should return to the counter. 3. Avoid missing class or having to come back because she lacks a requirement. |
| **Frustrations** | 1. Long, slow, crowded lines at the IIT cashier and Registrar. 2. Waiting in person without a clear way to know when her turn will come (there is only one line in the cashier). 3. Risking a missed class or deadline, or making another trip when a requirement is missing. |
| **Devices and context** | Primarily uses a smartphone browser to check service instructions. She may be on campus between classes or preparing for a visit. Whether she can join the queue remotely depends on the office's approved policy. |
| **Tech comfort** | Medium to high: she is comfortable with common mobile websites but should not need technical knowledge to get a ticket or understand her position. |
| **Accessibility needs** | No specific individual accessibility need was documented in the compiled Week 1 research. As a design precaution, use readable text, strong contrast, clear labels, keyboard-accessible controls, and status wording that does not rely on color alone. |

### Scenario

Aira arrives on campus to request an academic document before her next class. The Registrar queue is already crowded, and she cannot tell how long the wait will be. She opens Qonnect on her device, selects the appropriate document-request service, and reads the office's instructions before joining. If the service only permits in-person joining, she follows that rule and gets in line at the office; if remote joining is approved, she can request a ticket before walking over. She checks her ticket queueing app to see whether she is still waiting or has been called, so she can make a better decision about how to use the time without assuming the estimated wait is guaranteed.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Find the correct active service and read its instructions | Services / Join | FR-01 |
| Get a queue ticket for the selected service | Join | FR-02 |
| Check ticket status, queue position, and last-updated time | My ticket | FR-03 |

### What this means for my interface

1. Because students may not know which office service matches their need, my interface must show plain-language service names and instructions before ticket creation.
2. Because students currently wait without knowing when their turn will come, my interface must make the ticket code, current status, and number of people ahead easy to find.
3. Because waiting can conflict with classes and deadlines, my interface must refresh ticket status automatically, show when it was last updated, and label any wait-time figure (if there are any) as an estimate.


## Ramon Dela Cruz, the staff member

> "Hasol pud minsan sa amoang part nga ga-process mi ug transaction while gatubag sa mga pangutana sa mga estudyante bahin sa ilahang inquiries."

| | |
| --- | --- |
| **Photo or sketch** | [A drawing, an icon, or a free stock photo. Never a photo of the real person you interviewed.] |
| **Age, role and background** | 38, university office employee who handles a service counter for Registrar or Cashier transactions. |
| **Goals** | 1. Process students in a clear, consistent queue order. 2. Know which ticket is next and update each ticket correctly. 3. Help students understand where to go and what step to take next. |
| **Frustrations** | 1. Keeping track of the current queue while also handling transactions. 2. Repeating explanations about service types or requirements. 3. Confusion when a ticket holder is absent or a ticket status is not updated. |
| **Devices and context** | Uses an office desktop computer and the staff dashboard while working at a counter. He may be switching between the queue, student documents, and face-to-face questions. |
| **Tech comfort** | Medium: the design assumes he can use basic office software but should not have to learn a complicated queue-management workflow. |
| **Accessibility needs** | Provide readable table text, clear focus states, keyboard operation, large action targets, and explicit confirmation/error messages as general accessibility safeguards. |

### Scenario

At the start of a busy service period, Ramon opens Qonnect on the office computer and signs in to the queue system assigned to his counter. The day's requests fall within the project’s identified services: enrollment, document requests, payments and fees, student records, registration, and clearance verification, so he confirms the selected service before calling the next ticket. When a student is ready, he calls the ticket, serves the student, and updates the status when the transaction is complete. If the student is not present, he updates the queue status of the student appropriately  rather than making up a queue rule. The dashboard keeps the next eligible ticket and available actions visible so he can focus on the person at the counter.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Sign in before accessing queue controls | Staff login | FR-04 |
| Call the earliest eligible waiting ticket for the selected service | Staff queue | FR-05 |
| Update a ticket through a valid status change | Queue controls | FR-05 |

### What this means for my interface

1. Because the project covers multiple service types, my interface must keep the active service and counter unmistakably visible before staff call a ticket.
2. Because staff need to move tickets through a consistent workflow, my interface must make the next valid action easy to identify and prevent invalid status changes.
3. Because students' identities and private records should not be exposed on a public queue board, my interface must use ticket codes for public display and keep staff-only controls behind authentication.