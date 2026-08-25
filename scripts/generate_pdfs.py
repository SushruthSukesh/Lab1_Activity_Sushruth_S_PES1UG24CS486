import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header
        self.drawString(54, 750, "PES University - Dept. of CSE | Lab 1: Requirements Engineering & UML Use-Case Modelling")
        self.drawRightString(612 - 54, 750, "Problem Statement #55")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Student: Sushruth S | SRN: PES1UG24CS486 | Book Club Reading Challenge & Discussion Portal")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_requirements_table_pdf():
    doc = SimpleDocTemplate(
        "Requirements_Table.pdf",
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )
    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1E293B')
    )
    cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0F172A')
    )
    cell_priority_high = ParagraphStyle(
        'CellHigh',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#B91C1C'),
        alignment=1
    )
    cell_priority_med = ParagraphStyle(
        'CellMed',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#D97706'),
        alignment=1
    )

    story = []
    story.append(Paragraph("DELIVERABLE 1: Complete Requirements Specification Table", title_style))
    story.append(Paragraph("<b>Problem Statement #55:</b> Book Club Reading Challenge & Discussion Portal &nbsp;|&nbsp; <b>Student:</b> Sushruth S (PES1UG24CS486)", subtitle_style))
    story.append(Spacer(1, 4))

    table_data = [
        [
            Paragraph("<b>Req ID</b>", th_style),
            Paragraph("<b>Type</b>", th_style),
            Paragraph("<b>Description</b>", th_style),
            Paragraph("<b>Priority</b>", th_style),
            Paragraph("<b>Acceptance Criteria</b>", th_style),
            Paragraph("<b>Rationale (Justification)</b>", th_style),
            Paragraph("<b>Comments / Technical Notes</b>", th_style)
        ],
        # FR-001
        [
            Paragraph("<b>FR-001</b>", cell_bold),
            Paragraph("Functional", cell_style),
            Paragraph("The system shall hide content inside spoiler-tagged discussion comments until the user explicitly clicks to reveal or marks that chapter as read.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Spoiler text masked with blur filter.<br/><b>Fail:</b> Spoiler content exposed in search preview.", cell_style),
            Paragraph("Protects readers from inadvertent plot spoilers before finishing chapters.", cell_style),
            Paragraph("Implemented via client-side CSS blur mask with persistent user read-state sync.", cell_style)
        ],
        # FR-002
        [
            Paragraph("<b>FR-002</b>", cell_bold),
            Paragraph("Functional", cell_style),
            Paragraph("The system shall track individual user reading progress by logging daily/monthly page count goals and updating progress percentage toward the active challenge.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Progress bar increments immediately upon logging valid integer page count.<br/><b>Fail:</b> Negative values accepted or gauge fails to update.", cell_style),
            Paragraph("Core gamification mechanic to motivate members to complete scheduled reading milestones.", cell_style),
            Paragraph("Input validated against total book page bound; updates user dashboard asynchronously.", cell_style)
        ],
        # FR-003
        [
            Paragraph("<b>FR-003</b>", cell_bold),
            Paragraph("Functional", cell_style),
            Paragraph("The system shall allow Discussion Leads to create and moderate chapter-specific discussion threads with custom pinned discussion prompts.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Only verified Discussion Leads can pin/close threads or delete flagged comments.<br/><b>Fail:</b> Regular members access moderation controls.", cell_style),
            Paragraph("Facilitates structured, organized, and toxicity-free book analysis across chapters.", cell_style),
            Paragraph("Enforced using Role-Based Access Control (RBAC) on backend moderation API endpoints.", cell_style)
        ],
        # FR-004
        [
            Paragraph("<b>FR-004</b>", cell_bold),
            Paragraph("Functional", cell_style),
            Paragraph("The system shall allow Club Members to cast exactly one vote in the active monthly book selection poll from a curated list of nominated titles.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Member submits 1 vote, receives confirmation, voting controls disable.<br/><b>Fail:</b> Member submits multiple votes upon refresh.", cell_style),
            Paragraph("Ensures democratic, fair, and tamper-resistant book selection for upcoming reading cycles.", cell_style),
            Paragraph("Guaranteed by unique compound index (UserID + PollID) in persistence layer.", cell_style)
        ],
        # FR-005
        [
            Paragraph("<b>FR-005</b>", cell_bold),
            Paragraph("Functional", cell_style),
            Paragraph("The system shall award and display digital achievement badges on user profiles upon reaching predefined reading milestones (e.g., 500 pages logged).", cell_style),
            Paragraph("Medium", cell_priority_med),
            Paragraph("<b>Pass:</b> Badge icon renders in user profile showcase within 5s of milestone trigger.<br/><b>Fail:</b> Badge granted without reaching page goal.", cell_style),
            Paragraph("Increases long-term member engagement and social recognition within the club.", cell_style),
            Paragraph("Triggered via background event listener on goal progress update.", cell_style)
        ],
        # NFR-001
        [
            Paragraph("<b>NFR-001</b>", cell_bold),
            Paragraph("Non-Functional<br/>(Perf & Sec)", cell_style),
            Paragraph("Monthly poll voting results must prevent duplicate votes using user session verification and update tallies in real-time.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Benchmarking confirms latency &lt; 200ms and 0 duplicate votes under 1,000 peak users.<br/><b>Fail:</b> Duplicate vote accepted or lag &gt; 1.5s.", cell_style),
            Paragraph("Ensures poll data integrity and instantaneous community feedback during high-traffic voting.", cell_style),
            Paragraph("Utilizes in-memory Redis tally cache paired with transactional DB writes.", cell_style)
        ],
        # NFR-002
        [
            Paragraph("<b>NFR-002</b>", cell_bold),
            Paragraph("Non-Functional<br/>(Security & Availability)", cell_style),
            Paragraph("The portal shall maintain 99.9% system availability and encrypt all stored user reading history and credentials using AES-256 and SHA-256.", cell_style),
            Paragraph("High", cell_priority_high),
            Paragraph("<b>Pass:</b> Monthly uptime logs &ge; 99.9% and automated vulnerability scans confirm zero plaintext PII leaks.<br/><b>Fail:</b> Downtime &gt; 43.8 min/month.", cell_style),
            Paragraph("Protects member privacy, avoids credential compromise, and ensures reliable access during reading deadlines.", cell_style),
            Paragraph("Enforces TLS 1.3 in transit and column-level encryption at rest with automated health probes.", cell_style)
        ]
    ]

    col_widths = [46, 68, 120, 42, 108, 86, 70]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(t)
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Built Requirements_Table.pdf")


def build_use_case_flow_pdf():
    doc = SimpleDocTemplate(
        "Use_Case_Flow_Specification.pdf",
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'UCTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=2
    )
    sub_style = ParagraphStyle(
        'UCSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569'),
        spaceAfter=8
    )
    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=5,
        spaceAfter=3
    )
    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    story = []
    story.append(Paragraph("DELIVERABLE 3: Use-Case Flow Specification (1-Page Formal Document)", title_style))
    story.append(Paragraph("<b>Problem Statement #55:</b> Book Club Reading Challenge & Discussion Portal &nbsp;|&nbsp; <b>Author:</b> Sushruth S (PES1UG24CS486)", sub_style))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Use Case ID:</b>", body_bold), Paragraph("UC-04", body),
         Paragraph("<b>Use Case Name:</b>", body_bold), Paragraph("Vote in Monthly Book Selection Poll", body)],
        [Paragraph("<b>Primary Actor:</b>", body_bold), Paragraph("Club Member", body),
         Paragraph("<b>Secondary Actors:</b>", body_bold), Paragraph("Auth Service, Real-Time Tally Engine", body)],
        [Paragraph("<b>Trigger:</b>", body_bold), Paragraph("Member opens active monthly book poll", body),
         Paragraph("<b>Stereotypes:</b>", body_bold), Paragraph("«include» Session Verification, «include» Real-Time Tally", body)]
    ]
    meta_table = Table(meta_data, colWidths=[90, 176, 110, 156])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # Preconditions & Postconditions Table
    cond_data = [
        [
            Paragraph("<b>Preconditions:</b><br/>"
                      "1. Member must hold an authenticated, active account session on the portal.<br/>"
                      "2. An active monthly book selection poll must be open for voting.<br/>"
                      "3. Member has not yet submitted a vote in the current voting cycle.", body),
            Paragraph("<b>Postconditions:</b><br/>"
                      "1. Member's single vote is recorded and permanently bound to their profile.<br/>"
                      "2. Aggregated poll tallies and percentages update across all live sessions.<br/>"
                      "3. Member UI transitions to read-only confirmation state with disabled buttons.", body)
        ]
    ]
    cond_table = Table(cond_data, colWidths=[266, 266])
    cond_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(cond_table)
    story.append(Spacer(1, 3))

    # Main Success Scenario
    story.append(Paragraph("<b>Main Success Scenario (MSS):</b>", sec_head))
    mss_steps = [
        "1. <b>Navigate to Poll:</b> Club Member navigates to the 'Monthly Book Poll' section on the community dashboard.",
        "2. <b>Retrieve Details:</b> System fetches active nominees, book synopsis previews, and verifies the member's voting eligibility.",
        "3. <b>Display Options:</b> System displays nominated titles with interactive radio selection elements and current poll deadline.",
        "4. <b>Select Book:</b> Club Member selects their desired book candidate from the list.",
        "5. <b>Submit Ballot:</b> Club Member clicks the 'Submit Vote' button.",
        "6. <b>Confirm Intent:</b> System presents a confirmation modal: <i>'Confirm your vote for [Selected Book]? This cannot be changed.'</i>",
        "7. <b>Acknowledge:</b> Club Member confirms their selection.",
        "8. <b>Validate & Lock:</b> System verifies the session token and initiates an atomic write transaction to record the ballot.",
        "9. <b>Update Tallies:</b> System increments candidate score in Redis cache and pushes real-time websocket broadcast to active users.",
        "10. <b>Render Success State:</b> System presents a 'Vote Recorded Successfully' receipt, reveals live graphical percentage distribution, and locks member voting controls.",
        "11. <b>Conclusion:</b> Use case terminates successfully."
    ]
    for step in mss_steps:
        story.append(Paragraph(step, body))
        story.append(Spacer(1, 1.5))

    story.append(Spacer(1, 2))
    # Alternate Flows
    story.append(Paragraph("<b>Alternate / Exceptional Flows:</b>", sec_head))
    alt_flows = [
        "<b>3a. Member Has Already Voted in Active Cycle:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3a1. System detects existing vote timestamp in the member's profile for the active poll ID.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3a2. System displays current live results with notification: <i>'You have already voted in this cycle.'</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3a3. Voting controls remain permanently disabled. Use case terminates.",
        
        "<b>5a. Submission Without Selecting a Candidate:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5a1. System client-side validation detects empty selection upon clicking 'Submit Vote'.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5a2. System highlights the list in red with prompt: <i>'Please select one book before submitting.'</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5a3. Member selects a valid candidate and resumes at Step 5.",

        "<b>8a. Concurrent Session / Duplicate Vote Collision:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8a1. System database unique key constraint (UserID + PollID) detects a race-condition duplicate submission.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8a2. System rejects redundant payload, rolls back transaction, and returns HTTP 409 Conflict.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8a3. System displays alert: <i>'Duplicate vote prevented. Your previous vote is recorded.'</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8a4. System re-renders read-only results dashboard. Use case terminates.",

        "<b>8b. Poll Closes During User Interaction:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8b1. System detects current server timestamp is greater than poll expiration timestamp.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8b2. System rejects vote with notice: <i>'The voting window has closed. Thank you for participating.'</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;8b3. System transitions UI to final closed results leaderboard. Use case terminates."
    ]
    for alt in alt_flows:
        story.append(Paragraph(alt, body))
        story.append(Spacer(1, 2))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Built Use_Case_Flow_Specification.pdf")


def build_complete_combined_pdf():
    doc = SimpleDocTemplate(
        "Lab1_Complete_Deliverables_PES1UG24CS486.pdf",
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MasterTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'MasterSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        alignment=1,
        spaceAfter=12
    )
    sec_banner = ParagraphStyle(
        'Banner',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=8,
        spaceAfter=5
    )
    body = ParagraphStyle(
        'BodyM',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )
    
    story = []
    
    # Header Info
    story.append(Paragraph("PES University - Department of Computer Science & Engineering", title_style))
    story.append(Paragraph("<b>Lab 1: Requirements Engineering & UML Use-Case Modelling</b><br/>"
                           "<b>Problem Statement #55:</b> Book Club Reading Challenge & Discussion Portal<br/>"
                           "<b>Student Name:</b> Sushruth S &nbsp;|&nbsp; <b>SRN:</b> PES1UG24CS486 &nbsp;|&nbsp; <b>Semester:</b> 4th Sem CSE", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1E3A8A'), spaceAfter=8))

    # SECTION 1: Requirements Table
    story.append(Paragraph("1. Complete Requirements Specification Table (5 FRs, 2 NFRs)", sec_banner))
    
    th_style = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)
    cb = ParagraphStyle('CB', fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=colors.HexColor('#0F172A'))
    cs = ParagraphStyle('CS', fontName='Helvetica', fontSize=7, leading=8.5, textColor=colors.HexColor('#1E293B'))
    c_hi = ParagraphStyle('CHi', fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=colors.HexColor('#B91C1C'), alignment=1)
    c_md = ParagraphStyle('CMd', fontName='Helvetica-Bold', fontSize=7, leading=8.5, textColor=colors.HexColor('#D97706'), alignment=1)

    t_data = [
        [Paragraph("<b>Req ID</b>", th_style), Paragraph("<b>Type</b>", th_style), Paragraph("<b>Description</b>", th_style), Paragraph("<b>Priority</b>", th_style), Paragraph("<b>Acceptance Criteria</b>", th_style), Paragraph("<b>Rationale</b>", th_style), Paragraph("<b>Comments</b>", th_style)],
        [Paragraph("<b>FR-001</b>", cb), Paragraph("Functional", cs), Paragraph("The system shall hide content inside spoiler-tagged discussion comments until the user explicitly clicks to reveal or marks that chapter as read.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> Masked with blur filter.<br/><b>Fail:</b> Exposed in search preview.", cs), Paragraph("Protects readers from inadvertent plot spoilers.", cs), Paragraph("Client CSS mask + read-state sync.", cs)],
        [Paragraph("<b>FR-002</b>", cb), Paragraph("Functional", cs), Paragraph("The system shall track personal reading page goals and update progress toward active challenge.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> Gauge increments with valid pages.<br/><b>Fail:</b> Negative page count accepted.", cs), Paragraph("Gamifies community reading targets.", cs), Paragraph("Boundary validation against total pages.", cs)],
        [Paragraph("<b>FR-003</b>", cb), Paragraph("Functional", cs), Paragraph("The system shall allow Discussion Leads to create and moderate chapter-specific discussion threads.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> Leads can pin/close threads.<br/><b>Fail:</b> Regular members access lead actions.", cs), Paragraph("Ensures structured, safe book analysis.", cs), Paragraph("RBAC on moderation endpoints.", cs)],
        [Paragraph("<b>FR-004</b>", cb), Paragraph("Functional", cs), Paragraph("The system shall allow Club Members to cast exactly one vote in the active monthly book selection poll.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> 1 vote recorded, buttons lock.<br/><b>Fail:</b> Duplicate vote on refresh.", cs), Paragraph("Democratic, tamper-proof book choice.", cs), Paragraph("Compound index (UserID+PollID).", cs)],
        [Paragraph("<b>FR-005</b>", cb), Paragraph("Functional", cs), Paragraph("The system shall award digital badges upon reaching reading milestone goals (e.g. 500 pages).", cs), Paragraph("Medium", c_md), Paragraph("<b>Pass:</b> Badge shows within 5s of milestone.<br/><b>Fail:</b> Badge granted without goal.", cs), Paragraph("Increases engagement & retention.", cs), Paragraph("Asynchronous milestone trigger.", cs)],
        [Paragraph("<b>NFR-001</b>", cb), Paragraph("Non-Func<br/>(Perf & Sec)", cs), Paragraph("Monthly poll voting must prevent duplicate votes with session verification & real-time tallies.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> Latency &lt; 200ms at 1,000 peak users.<br/><b>Fail:</b> Duplicate vote or lag &gt; 1.5s.", cs), Paragraph("Guarantees poll integrity & speed.", cs), Paragraph("Redis cache + atomic DB transaction.", cs)],
        [Paragraph("<b>NFR-002</b>", cb), Paragraph("Non-Func<br/>(Sec & Avail)", cs), Paragraph("System shall maintain 99.9% uptime and encrypt credentials and history using AES-256 / SHA-256.", cs), Paragraph("High", c_hi), Paragraph("<b>Pass:</b> Uptime &ge; 99.9%, zero PII leak.<br/><b>Fail:</b> Monthly downtime &gt; 43.8 min.", cs), Paragraph("Ensures privacy and high reliability.", cs), Paragraph("TLS 1.3 + column encryption at rest.", cs)]
    ]

    t_combined = Table(t_data, colWidths=[42, 60, 126, 40, 112, 90, 70])
    t_combined.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_combined)
    story.append(PageBreak())

    # SECTION 2: UML Diagram
    story.append(Paragraph("2. UML Use-Case Diagram", sec_banner))
    story.append(Paragraph("The diagram models all core actors (Club Member, Discussion Lead, Authentication & Backend System) and primary use cases (UC-01 to UC-05), incorporating both <b>«include»</b> (session verification, real-time tally) and <b>«extend»</b> (spoiler reveal, milestone badge award) relationships along with actor generalization.", body))
    story.append(Spacer(1, 6))
    
    if os.path.exists("Use_Case_Diagram.png"):
        story.append(Image("Use_Case_Diagram.png", width=530, height=380))
    story.append(PageBreak())

    # SECTION 3: Use Case Flow Specification
    story.append(Paragraph("3. Use-Case Flow Specification: UC-04 (Vote in Monthly Book Selection Poll)", sec_banner))
    
    flow_meta = [
        [Paragraph("<b>Use Case ID:</b>", cb), Paragraph("UC-04", cs), Paragraph("<b>Use Case Name:</b>", cb), Paragraph("Vote in Monthly Book Selection Poll", cs)],
        [Paragraph("<b>Primary Actor:</b>", cb), Paragraph("Club Member", cs), Paragraph("<b>Secondary Actors:</b>", cb), Paragraph("Auth Service, Real-Time Tally Engine", cs)],
        [Paragraph("<b>Stereotypes:</b>", cb), Paragraph("«include» Session Verification, «include» Real-Time Tally", cs), Paragraph("<b>Priority:</b>", cb), Paragraph("High (Core Democratic Feature)", cs)]
    ]
    flow_meta_tbl = Table(flow_meta, colWidths=[80, 180, 100, 180])
    flow_meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(flow_meta_tbl)
    story.append(Spacer(1, 4))

    conds = [
        [
            Paragraph("<b>Preconditions:</b><br/>"
                      "1. User is authenticated with active session.<br/>"
                      "2. Monthly book selection poll is active and open.<br/>"
                      "3. Member has not yet voted in current cycle.", cs),
            Paragraph("<b>Postconditions:</b><br/>"
                      "1. Member's single vote is recorded and permanently bound.<br/>"
                      "2. Live aggregate tallies update across all active user sessions.<br/>"
                      "3. Member UI transitions to locked read-only results view.", cs)
        ]
    ]
    cond_tbl = Table(conds, colWidths=[270, 270])
    cond_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(cond_tbl)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Main Success Scenario (MSS):</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1E3A8A'))))
    mss = [
        "1. <b>Navigate to Poll:</b> Member navigates to the 'Monthly Book Poll' section on dashboard.",
        "2. <b>Retrieve Details:</b> System retrieves active poll candidates, synopsis, and checks voting status.",
        "3. <b>Display Nominees:</b> System renders nominated books with selection radio options.",
        "4. <b>Select Candidate:</b> Member selects their preferred book title.",
        "5. <b>Submit Vote:</b> Member clicks 'Submit Vote'.",
        "6. <b>Confirm Modal:</b> System displays confirmation modal (<i>'Confirm vote for [Book Title]?'</i>).",
        "7. <b>Acknowledge:</b> Member confirms selection.",
        "8. <b>Validate & Persist:</b> System checks user session and performs atomic write transaction.",
        "9. <b>Update Tallies:</b> System updates Redis real-time count and emits websocket broadcast.",
        "10. <b>Render Confirmation:</b> System displays success banner and locks member voting controls.",
        "11. <b>Termination:</b> Use case completes successfully."
    ]
    for s in mss:
        story.append(Paragraph(s, cs))
        story.append(Spacer(1, 1))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Alternate / Exceptional Flows:</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#1E3A8A'))))
    alts = [
        "<b>3a. Already Voted in Cycle:</b> System identifies prior vote &rarr; Displays live percentage chart & disables vote button &rarr; Terminates.",
        "<b>5a. Empty Selection Submitted:</b> Member clicks submit without choice &rarr; System highlights options in red & prompts selection &rarr; Resumes Step 5.",
        "<b>8a. Duplicate Submission Collision:</b> Database unique key constraint flags collision &rarr; System rolls back and returns 409 Conflict &rarr; Displays alert &rarr; Terminates.",
        "<b>8b. Poll Expiration During Voting:</b> System detects poll deadline passed &rarr; Informs user poll has closed &rarr; Redirects to final results &rarr; Terminates."
    ]
    for a in alts:
        story.append(Paragraph(a, cs))
        story.append(Spacer(1, 1.5))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Built Lab1_Complete_Deliverables_PES1UG24CS486.pdf")

if __name__ == "__main__":
    build_requirements_table_pdf()
    build_use_case_flow_pdf()
    build_complete_combined_pdf()
