import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_use_case_diagram():
    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Color Palette
    bg_color = "#F8FAFC"
    border_color = "#334155"
    box_bg = "#FFFFFF"
    primary_uc_color = "#EFF6FF"
    primary_uc_border = "#2563EB"
    rel_uc_color = "#FEF3C7"
    rel_uc_border = "#D97706"
    actor_color = "#1E293B"
    text_color = "#0F172A"

    fig.patch.set_facecolor(bg_color)

    # Title Header
    ax.text(7.5, 10.5, "UML Use-Case Diagram: Book Club Reading Challenge & Discussion Portal", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1E3A8A')
    ax.text(7.5, 10.15, "Problem Statement #55 | Student: Sushruth S (PES1UG24CS486) | Dept. of CSE, PES University", 
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#475569')

    # System Boundary Box
    sys_rect = patches.FancyBboxPatch((3.4, 0.6), 8.2, 9.2,
                                     boxstyle="round,pad=0.2",
                                     edgecolor=border_color, facecolor=box_bg, linewidth=2, linestyle='-')
    ax.add_patch(sys_rect)
    ax.text(3.7, 9.55, "System Boundary: Book Club Portal", fontsize=11, fontweight='bold', color="#1E293B")

    # Helper function to draw stick figure actor
    def draw_actor(x, y, name, role=""):
        # Head
        head = patches.Circle((x, y + 0.45), 0.22, edgecolor=actor_color, facecolor="#DBEAFE", linewidth=2)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 0.23, y - 0.25], color=actor_color, linewidth=2)
        # Arms
        ax.plot([x - 0.35, x + 0.35], [y + 0.08, y + 0.08], color=actor_color, linewidth=2)
        # Legs
        ax.plot([x, x - 0.28], [y - 0.25, y - 0.65], color=actor_color, linewidth=2)
        ax.plot([x, x + 0.28], [y - 0.25, y - 0.65], color=actor_color, linewidth=2)
        # Label
        ax.text(x, y - 0.82, name, ha='center', va='top', fontsize=10, fontweight='bold', color='#0F172A')
        if role:
            ax.text(x, y - 1.02, f"«{role}»", ha='center', va='top', fontsize=8, fontstyle='italic', color='#64748B')

    # Helper function to draw use case oval
    def draw_use_case(x, y, w, h, code, title, is_stereotype=False):
        edge_c = rel_uc_border if is_stereotype else primary_uc_border
        face_c = rel_uc_color if is_stereotype else primary_uc_color
        ellipse = patches.Ellipse((x, y), w, h, edgecolor=edge_c, facecolor=face_c, linewidth=1.8, zorder=3)
        ax.add_patch(ellipse)
        full_text = f"{code}\n{title}" if code else title
        ax.text(x, y, full_text, ha='center', va='center', fontsize=8.5, fontweight='bold' if not is_stereotype else 'normal', color=text_color, zorder=4)

    # Draw Actors
    draw_actor(1.6, 7.8, "Club Member", "Primary Actor")
    draw_actor(1.6, 2.8, "Discussion Lead", "Specialized Actor")
    draw_actor(13.4, 5.5, "Authentication &\nBackend System", "Secondary Actor")

    # Generalization line from Discussion Lead to Club Member
    ax.annotate("", xy=(1.6, 6.5), xytext=(1.6, 4.0),
                arrowprops=dict(facecolor='white', edgecolor='#475569', width=1.5, headwidth=9, headlength=10))
    ax.text(0.65, 5.25, "«inherits/specializes»", fontsize=7.5, color="#64748B", rotation=90, va='center')

    # Primary Use Cases (in center)
    uc_data = [
        (5.8, 8.7, 3.2, 0.95, "UC-01", "Set & Track\nReading Goals"),
        (5.8, 6.9, 3.2, 0.95, "UC-02", "Participate in Chapter\nDiscussion Thread"),
        (5.8, 5.1, 3.2, 0.95, "UC-03", "Create & Moderate\nDiscussion Thread"),
        (5.8, 3.3, 3.2, 0.95, "UC-04", "Vote in Monthly\nBook Selection Poll"),
        (5.8, 1.5, 3.2, 0.95, "UC-05", "Create & Manage\nMonthly Poll"),
    ]

    for x, y, w, h, code, title in uc_data:
        draw_use_case(x, y, w, h, code, title)

    # Stereotyped Use Cases («include» and «extend»)
    draw_use_case(9.8, 8.7, 2.7, 0.9, "UC-06", "Award Milestone\nBadge", is_stereotype=True)
    draw_use_case(9.8, 6.9, 2.7, 0.9, "UC-07", "Reveal Spoiler\nContent", is_stereotype=True)
    draw_use_case(9.8, 4.2, 2.7, 0.9, "UC-08", "Verify User Session\n& Authenticate", is_stereotype=True)
    draw_use_case(9.8, 2.1, 2.7, 0.9, "UC-09", "Tally & Publish\nReal-Time Results", is_stereotype=True)

    # Actor to Use Case Associations (Solid lines)
    # Club Member to UC-01, UC-02, UC-04
    ax.plot([1.9, 4.2], [7.8, 8.7], color='#334155', linewidth=1.4)
    ax.plot([1.9, 4.2], [7.8, 6.9], color='#334155', linewidth=1.4)
    ax.plot([1.9, 4.2], [7.4, 3.5], color='#334155', linewidth=1.4)

    # Discussion Lead to UC-03, UC-05
    ax.plot([1.9, 4.2], [2.8, 5.1], color='#334155', linewidth=1.4)
    ax.plot([1.9, 4.2], [2.8, 1.6], color='#334155', linewidth=1.4)

    # Secondary Actor to UC-08, UC-09
    ax.plot([13.1, 11.2], [5.5, 4.3], color='#334155', linewidth=1.4)
    ax.plot([13.1, 11.2], [5.3, 2.2], color='#334155', linewidth=1.4)

    # «extend» Relationships (Dashed arrow from extension to base)
    # UC-06 -> UC-01 («extend» when reading goal milestone reached)
    ax.annotate("", xy=(7.4, 8.7), xytext=(8.45, 8.7),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#D97706", lw=1.6))
    ax.text(7.9, 8.95, "«extend»", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#D97706")

    # UC-07 -> UC-02 («extend» when user clicks to unmask spoiler)
    ax.annotate("", xy=(7.4, 6.9), xytext=(8.45, 6.9),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#D97706", lw=1.6))
    ax.text(7.9, 7.15, "«extend»", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#D97706")

    # «include» Relationships (Dashed arrow from base to included)
    # UC-04 -> UC-08 («include» session verification for voting)
    ax.annotate("", xy=(8.55, 3.8), xytext=(7.3, 3.5),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#2563EB", lw=1.6))
    ax.text(7.7, 3.85, "«include»", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#2563EB", rotation=14)

    # UC-02 -> UC-08 («include» session verification for commenting)
    ax.annotate("", xy=(8.55, 4.6), xytext=(7.2, 6.5),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#2563EB", lw=1.6))
    ax.text(8.0, 5.75, "«include»", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#2563EB", rotation=-32)

    # UC-04 -> UC-09 («include» real-time tally update upon vote submission)
    ax.annotate("", xy=(8.55, 2.35), xytext=(7.3, 3.1),
                arrowprops=dict(arrowstyle="->", linestyle="dashed", color="#2563EB", lw=1.6))
    ax.text(7.75, 2.5, "«include»", ha='center', va='bottom', fontsize=8, fontweight='bold', color="#2563EB", rotation=-18)

    # Legend Box
    leg_rect = patches.FancyBboxPatch((0.4, 0.2), 3.0, 1.4,
                                      boxstyle="round,pad=0.1",
                                      edgecolor="#CBD5E1", facecolor="#FFFFFF", linewidth=1)
    ax.add_patch(leg_rect)
    ax.text(0.5, 1.45, "Legend / UML Conventions:", fontsize=8, fontweight='bold', color="#1E293B")
    ax.text(0.5, 1.15, "——  Association (Actor to Use Case)", fontsize=7.5, color="#334155")
    ax.text(0.5, 0.85, "- - > «include» (Mandatory Sub-flow)", fontsize=7.5, color="#2563EB")
    ax.text(0.5, 0.55, "- - > «extend» (Conditional Sub-flow)", fontsize=7.5, color="#D97706")
    ax.text(0.5, 0.25, "——▷ Generalization / Specialization", fontsize=7.5, color="#475569")

    plt.tight_layout()
    plt.savefig("Use_Case_Diagram.png", dpi=300, bbox_inches='tight')
    plt.savefig("Use_Case_Diagram.pdf", bbox_inches='tight')
    plt.close()
    print("Successfully generated Use_Case_Diagram.png and Use_Case_Diagram.pdf")

if __name__ == "__main__":
    draw_use_case_diagram()
