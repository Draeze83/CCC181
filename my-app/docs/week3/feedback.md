## Screen 1: Services / Join

**Works well:** Service names are understandable, and office instructions appear before the Join Queue button. This follows the persona's design rule of showing service details before ticket creation.

**Problem:** The selected service is unclear, and the OPEN / CLOSED status is only a placeholder. The four service categories also combine different services and omit familiar labels like "Cashier" and "Registrar," making it harder for Aira to find the right service.

**Change:**
- Add a visible "✓ Selected" marker to the chosen service.
- Show the actual service status beside the Join Queue button and disable it when closed.
- Keep office instructions above the Join Queue button.

---

## Screen 2: My Ticket

**Works well:** The ticket number and number of people ahead are prominent. The status uses text, the waiting-time estimate has a disclaimer, and the last-updated time is displayed.

**Problem:** The phone's status is less prominent and lacks an auto-refresh notice. The indicated counter is not specified, and there is no guidance for missed calls.

**Change:**
- Make the ticket status a prominent box on the phone and add "Auto-refreshes every 10 seconds."
- Show the assigned counter when the ticket is called.
- Add a missed-call instruction based on approved office policy.


---

## Screen 3: Staff Queue Dashboard

**Works well:** Service and counter selectors appear at the top, helping Ramon confirm the correct queue. The Call Next and Mark Served buttons are prominent and easy to reach.

**Problem:** The same ticket appears as both WAITING and BEING SERVED, and the buttons remain active simultaneously. The dashboard lacks a clear Skip / No-show action, the View action is unclear, and the phone's waiting list does not provide usable controls.

**Change:**
- Show consistent ticket states and disable actions when they are invalid.
- Display "No ticket being served" when appropriate.
- Add a visible Skip / No-show button governed by approved office policy.
- Replace or remove the unclear View action.
- Make the phone waiting list as actionable as the laptop table.
- Keep service and counter selectors at the top.