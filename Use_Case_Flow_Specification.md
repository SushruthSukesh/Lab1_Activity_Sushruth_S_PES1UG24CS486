# Deliverable 3: Use-Case Flow Specification

**Institution:** PES University — Department of Computer Science & Engineering  
**Course:** Lab 1: Requirements Engineering & UML Use-Case Modelling  
**Problem Statement #55:** Book Club Reading Challenge & Discussion Portal  
**Student Name:** Sushruth S  
**SRN:** PES1UG24CS486  

---

## 1. Use Case Identification

| Attribute | Details |
| :--- | :--- |
| **Use Case ID** | **UC-04** |
| **Use Case Name** | **Vote in Monthly Book Selection Poll** |
| **Primary Actor** | **Club Member** |
| **Secondary Actors** | **Authentication Service**, **Real-Time Poll Tally Engine** |
| **Stereotypes / Relations** | `«include»` Verify User Session & Authenticate (UC-08)<br>`«include»` Tally & Publish Real-Time Results (UC-09) |
| **Priority** | High |
| **Trigger** | Member clicks "Vote in Active Poll" on the community portal dashboard |

---

## 2. Preconditions & Postconditions

### Preconditions
1. The Club Member must hold an authenticated, active account session on the portal.
2. A monthly book selection poll must currently be active and open for member voting.
3. The Club Member must not have previously cast a ballot in the current active poll cycle.

### Postconditions
1. The member's single vote is recorded and permanently bound to their profile for this cycle.
2. Real-time aggregate tallies and candidate percentages are incremented across all active client views.
3. The member's user interface transitions to a read-only confirmation state with voting controls permanently disabled.

---

## 3. Main Success Scenario (MSS)

```mermaid
sequenceDiagram
    autonumber
    actor Member as Club Member
    participant UI as Portal Frontend
    participant Auth as Auth & Session Service
    participant Poll as Poll & Tally Engine
    participant DB as Persistent Database

    Member->>UI: 1. Navigate to "Monthly Book Selection Poll"
    UI->>Auth: 2. Validate session & check prior voting status
    Auth-->>UI: Session valid; Member has not yet voted
    UI->>Poll: 3. Fetch active nominees & summaries
    Poll-->>UI: Return nominee list & current standings
    UI-->>Member: 4. Display nominated books & selection options
    Member->>UI: 5. Select preferred book candidate
    Member->>UI: 6. Click "Submit Vote"
    UI-->>Member: 7. Display Confirmation Modal ("Confirm vote for [Title]?")
    Member->>UI: 8. Confirm selection
    UI->>Poll: 9. Post ballot payload with signed session token
    Poll->>DB: 10. Execute atomic ballot write (UserID + PollID)
    DB-->>Poll: 11. Write committed successfully
    Poll->>Poll: 12. Increment candidate tally in Redis cache & publish WebSocket event
    Poll-->>UI: 13. Return success receipt & updated live percentage tallies
    UI-->>Member: 14. Display "Vote Recorded!" badge & lock voting interface
```

### Detailed Step-by-Step Flow:
1. **Navigate to Poll:** The Club Member navigates to the **Monthly Book Poll** section from the portal dashboard.
2. **Retrieve Details:** The system retrieves the active poll metadata, nominated book titles, synopsis previews, and verifies the member's voting eligibility.
3. **Display Nominees:** The system renders the nominated book options with interactive radio selection elements and remaining time until close.
4. **Select Candidate:** The Club Member selects their desired book title from the nominee list.
5. **Submit Ballot:** The Club Member clicks the **"Submit Vote"** button.
6. **Confirm Intent:** The system prompts the user with a confirmation modal: *"Confirm your vote for '[Book Title]'? Once submitted, your vote cannot be modified."*
7. **Acknowledge:** The Club Member confirms the prompt.
8. **Validate & Persist:** The system invokes session verification (`«include»`) and executes an atomic write transaction ensuring single-ballot integrity.
9. **Update Tallies:** The system increments the candidate score (`«include»`), updates the Redis in-memory tally cache, and broadcasts real-time updates via WebSockets.
10. **Render Success State:** The system presents a *"Vote Recorded Successfully"* receipt, unveils updated real-time percentage charts, and locks member voting controls.
11. **Conclusion:** Use case terminates successfully.

---

## 4. Alternate & Exceptional Flows

### **3a. Member Has Already Voted in Current Cycle**
* **3a1.** System detects an existing vote record timestamp associated with the member's account for the active Poll ID.
* **3a2.** System displays the live poll distribution chart alongside an informational badge: *"You have already cast your vote for this cycle."*
* **3a3.** Voting buttons and selection inputs remain disabled. Use case terminates.

### **5a. Submission Attempt Without Candidate Selection**
* **5a1.** Member clicks "Submit Vote" without selecting any radio candidate option.
* **5a2.** Client-side validation intercepts the action and highlights the book list in red with an inline warning: *"Please select a nominated book before submitting."*
* **5a3.** Member selects a candidate book and resumes at Step 5.

### **8a. Concurrent Session / Duplicate Vote Collision**
* **8a1.** Database compound unique key constraint (`UserID_PollID`) catches a race-condition duplicate submission attempt across multiple tabs or devices.
* **8a2.** System rejects the second payload, rolls back write transaction, and responds with `HTTP 409 Conflict`.
* **8a3.** System displays alert: *"Duplicate vote rejected. Your prior vote is safely recorded."*
* **8a4.** UI refreshes to display the read-only live results dashboard. Use case terminates.

### **8b. Poll Closes During User Interaction**
* **8b1.** Server timestamp validation identifies that the poll deadline expired while the user was deliberating.
* **8b2.** System rejects ballot submission with notification: *"The voting window for this poll has just closed."*
* **8b3.** System redirects the member to the final results announcement leaderboard. Use case terminates.
