
import json
from pathlib import Path
from datetime import datetime, date
import html

import streamlit as st

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Careerly | Job Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

FILE_NAME = Path(__file__).with_name("applications.json")

VALID_STATUS = [
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
]

STATUS_STYLE = {
    "applied": ("#DBEAFE", "#1D4ED8"),
    "interview": ("#F3E8FF", "#7E22CE"),
    "offer": ("#DCFCE7", "#15803D"),
    "rejected": ("#FEE2E2", "#B91C1C"),
    "withdrawn": ("#E2E8F0", "#475569"),
}


# --------------------------------------------------
# DATA
# --------------------------------------------------

def load_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        for app in data:
            while len(app) < 5:
                app.append("")

        return data

    except FileNotFoundError:
        return []

    except (json.JSONDecodeError, OSError):
        st.error("Unable to read applications.json.")
        return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def parse_date(value):
    try:
        return datetime.strptime(value, "%d-%m-%Y").date()
    except (ValueError, TypeError):
        return None


def badge(status):
    bg, fg = STATUS_STYLE.get(
        status.lower(), ("#F1F5F9", "#334155")
    )
    label = html.escape(status.title())

    return (
        f'<span style="display:inline-block;'
        f'background:{bg};color:{fg};'
        f'padding:5px 11px;border-radius:20px;'
        f'font-size:12px;font-weight:650;'
        f'white-space:nowrap;">{label}</span>'
    )


# --------------------------------------------------
# DESIGN SYSTEM
# --------------------------------------------------

st.markdown("""
<style>
    :root {
        --navy: #17243D;
        --blue: #3977F6;
        --ink: #172033;
        --muted: #788399;
        --line: #E7EBF2;
        --canvas: #F5F7FB;
        --white: #FFFFFF;
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,251,0.95);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #17243D;
        border-right: 0;
    }

    [data-testid="stSidebar"] * {
        color: #E8EEF9;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #C0CBDE;
    }

    [data-testid="stSidebar"] hr {
        border-color: #34415A;
    }

    h1, h2, h3 {
        color: #172033;
        letter-spacing: -0.035em;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 750 !important;
    }

    h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 650 !important;
    }

    p, label {
        color: #344054;
    }

    .brand {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: white;
        padding: 8px 0 2px;
    }

    .brand-sub {
        color: #AAB8CF;
        font-size: 12px;
        margin-bottom: 24px;
    }

    .eyebrow {
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        color: #8290A7;
        margin-bottom: 7px;
    }

    .subtitle {
        color: #788399;
        font-size: 14px;
        margin-top: -9px;
        margin-bottom: 20px;
    }

    .section-label {
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1px;
        color: #8290A7;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E7EBF2;
        border-radius: 15px;
        padding: 20px 20px 16px;
        box-shadow: 0 3px 12px rgba(22, 34, 59, 0.025);
    }

    div[data-testid="stMetricLabel"] {
        color: #788399;
        font-size: 13px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #172033;
        font-size: 31px;
        font-weight: 750;
    }

    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #E7EBF2;
        border-radius: 15px;
        padding: 22px;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stDateInput"] input {
        border-radius: 9px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 40px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E7EBF2;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] {
        background: white;
        border: 1px solid #E7EBF2;
        border-radius: 13px;
    }

    .table-head {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.7px;
        color: #8994A8;
        padding-bottom: 9px;
    }

    .company-name {
        font-size: 13px;
        font-weight: 750;
        color: #172033;
        overflow-wrap: anywhere;
    }

    .role-name {
        font-size: 12px;
        color: #788399;
        overflow-wrap: anywhere;
    }

    .date-text {
        font-size: 12px;
        color: #475467;
    }

    .table-row {
        background: white;
        border-top: 1px solid #EDF0F5;
        padding-top: 12px;
        padding-bottom: 12px;
    }

    .small-note {
        color: #8994A8;
        font-size: 12px;
    }

    .welcome-card {
        background: linear-gradient(120deg, #EAF1FF, #F5F0FF);
        border: 1px solid #DCE6FB;
        border-radius: 15px;
        padding: 19px 22px;
        margin-bottom: 22px;
    }

    .welcome-title {
        color: #17243D;
        font-size: 17px;
        font-weight: 750;
    }

    .welcome-copy {
        color: #62718B;
        font-size: 13px;
        margin-top: 5px;
    }

    hr {
        border-color: #E7EBF2;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">✦ Careerly</div>'
        '<div class="brand-sub">YOUR CAREER, ORGANIZED</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "All Applications",
            "Add Application",
            "Follow-ups",
            "Statistics",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.markdown(
        '<div style="color:#AAB8CF;font-size:12px;">'
        'JOB SEARCH WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="color:#8393AD;font-size:11px;'
        'margin-top:16px;">'
        'Keep applying. Keep improving.</div>',
        unsafe_allow_html=True,
    )


applications = load_data()
today = date.today()


# --------------------------------------------------
# SHARED STATISTICS
# --------------------------------------------------

total = len(applications)
active = sum(
    1 for a in applications
    if a[2] in ("applied", "interview")
)
interviews = sum(1 for a in applications if a[2] == "interview")
offers = sum(1 for a in applications if a[2] == "offer")


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.markdown(
    '<div class="eyebrow">CAREER MANAGEMENT</div>',
    unsafe_allow_html=True,
)

st.title(
    {
        "Dashboard": "Your job search, at a glance",
        "All Applications": "All applications",
        "Add Application": "Add a new application",
        "Follow-ups": "Follow-up center",
        "Statistics": "Application analytics",
    }[page]
)

st.markdown(
    '<div class="subtitle">'
    'A clear view of your progress, opportunities and next steps.'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# APPLICATION TABLE COMPONENT
# --------------------------------------------------

def show_table(items):
    if not items:
        st.info(
            "No applications found. Try changing your filters "
            "or add a new application."
        )
        return

    st.markdown(
        '<div class="table-head">YOUR APPLICATION PIPELINE</div>',
        unsafe_allow_html=True,
    )

    headers = st.columns([1.65, 1.8, 1.12, 1.05, 1.15])

    for col, name in zip(
        headers,
        ["COMPANY", "POSITION", "STATUS", "APPLIED", "FOLLOW-UP"],
    ):
        col.markdown(
            f'<div class="table-head">{name}</div>',
            unsafe_allow_html=True,
        )

    for index, app in items:
        row = st.columns([1.65, 1.8, 1.12, 1.05, 1.15])

        with row[0]:
            st.markdown(
                f'<div class="company-name">'
                f'{html.escape(app[0])}</div>',
                unsafe_allow_html=True,
            )

        with row[1]:
            st.markdown(
                f'<div class="role-name">'
                f'{html.escape(app[1])}</div>',
                unsafe_allow_html=True,
            )

        with row[2]:
            st.markdown(badge(app[2]), unsafe_allow_html=True)

        with row[3]:
            st.markdown(
                f'<div class="date-text">'
                f'{html.escape(app[3] or "—")}</div>',
                unsafe_allow_html=True,
            )

        with row[4]:
            st.markdown(
                f'<div class="date-text">'
                f'{html.escape(app[4] or "—")}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div style="height:1px;background:#EDF0F5;'
            'margin:7px 0 12px 0;"></div>',
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="welcome-card">'
        '<div class="welcome-title">Welcome back 👋</div>'
        '<div class="welcome-copy">'
        'Small steps lead to big opportunities. '
        'Keep your application pipeline moving.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Your overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total applications", total)
    c2.metric("Active pipeline", active)
    c3.metric("Interviews", interviews)
    c4.metric("Offers", offers)

    st.write("")

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown("#### Recent applications")

        recent = list(enumerate(applications))[-5:][::-1]
        show_table(recent)

        if st.button("View all applications →"):
            st.session_state["navigate_all"] = True
            st.rerun()

    with right:
        st.markdown("#### Pipeline breakdown")

        if total:
            for status in VALID_STATUS:
                count = sum(1 for a in applications if a[2] == status)
                percentage = count / total

                st.markdown(
                    f'<div style="display:flex;justify-content:'
                    f'space-between;align-items:center;'
                    f'margin-top:16px;margin-bottom:6px;">'
                    f'<span>{badge(status)}</span>'
                    f'<span style="font-weight:700;color:#344054;">'
                    f'{count}</span></div>',
                    unsafe_allow_html=True,
                )

                st.progress(percentage)

        else:
            st.info("Add your first application to see your pipeline.")

        st.write("")
        st.markdown("#### Next steps")

        due_count = sum(
            1 for a in applications
            if parse_date(a[4]) is not None
            and parse_date(a[4]) <= today
        )

        st.caption(f"Follow-ups due: {due_count}")

        if st.button("Open follow-ups", use_container_width=True):
            st.session_state["navigate_followups"] = True
            st.rerun()


# --------------------------------------------------
# ALL APPLICATIONS
# --------------------------------------------------

elif page == "All Applications":

    c1, c2 = st.columns([2, 1])

    with c1:
        search = st.text_input(
            "Search",
            placeholder="Search by company or job role...",
        )

    with c2:
        status_filter = st.selectbox(
            "Status",
            ["all"] + VALID_STATUS,
            format_func=lambda s: (
                "All statuses" if s == "all" else s.title()
            ),
        )

    filtered = []

    for i, app in enumerate(applications):
        query = search.strip().lower()

        matches_text = (
            query in app[0].lower()
            or query in app[1].lower()
        )

        matches_status = (
            status_filter == "all" or app[2] == status_filter
        )

        if matches_text and matches_status:
            filtered.append((i, app))

    st.caption(f"{len(filtered)} applications shown")
    show_table(filtered)

    st.divider()
    st.markdown("#### Manage an application")

    if applications:
        options = [
            f"{i + 1}. {a[0]} — {a[1]}"
            for i, a in enumerate(applications)
        ]

        selected = st.selectbox("Select record", options)
        index = options.index(selected)

        left, right = st.columns(2)

        with left:
            new_status = st.selectbox(
                "New status",
                VALID_STATUS,
                index=VALID_STATUS.index(applications[index][2])
                if applications[index][2] in VALID_STATUS else 0,
                key="edit_status",
            )

            if st.button("Save status", use_container_width=True):
                applications[index][2] = new_status
                save_data(applications)
                st.success("Status updated.")
                st.rerun()

        with right:
            st.write("")

            confirm = st.checkbox(
                "Confirm permanent deletion",
                key="delete_confirm",
            )

            if st.button("Delete application", use_container_width=True):
                if confirm:
                    deleted = applications.pop(index)
                    save_data(applications)
                    st.success(f"Deleted {deleted[0]}.")
                    st.rerun()
                else:
                    st.warning("Check the confirmation box first.")


# --------------------------------------------------
# ADD APPLICATION
# --------------------------------------------------

elif page == "Add Application":

    st.markdown(
        "Enter the details below. Required fields are company and role."
    )

    with st.form("add_application_form", clear_on_submit=True):

        left, right = st.columns(2)

        with left:
            company = st.text_input(
                "Company name *",
                placeholder="e.g. Razorpay",
            )

            role = st.text_input(
                "Job role *",
                placeholder="e.g. Python Intern",
            )

            status = st.selectbox("Application status", VALID_STATUS)

        with right:
            appl_date = st.date_input(
                "Application date",
                value=today,
                format="DD-MM-YYYY",
            )

            has_followup = st.checkbox("Set a follow-up date")

            follow_date = None

            if has_followup:
                follow_date = st.date_input(
                    "Follow-up date",
                    value=today,
                    format="DD-MM-YYYY",
                )

        submitted = st.form_submit_button(
            "Save application",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not company.strip() or not role.strip():
                st.error("Company name and job role are required.")

            elif follow_date and follow_date < appl_date:
                st.error("Follow-up cannot be before the application date.")

            else:
                follow_text = (
                    follow_date.strftime("%d-%m-%Y")
                    if follow_date else ""
                )

                applications.append([
                    company.strip(),
                    role.strip(),
                    status,
                    appl_date.strftime("%d-%m-%Y"),
                    follow_text,
                ])

                save_data(applications)
                st.success("Application added successfully.")
                st.rerun()


# --------------------------------------------------
# FOLLOW-UPS
# --------------------------------------------------

elif page == "Follow-ups":

    due = []
    upcoming = []

    for i, app in enumerate(applications):
        follow = parse_date(app[4])

        if follow is None:
            continue

        item = {
            "Company": app[0],
            "Role": app[1],
            "Follow-up date": app[4],
            "Status": app[2].title(),
        }

        if follow <= today:
            due.append(item)

        elif (follow - today).days <= 7:
            upcoming.append(item)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Due today or overdue")
        st.caption(f"{len(due)} follow-ups need attention")

        if due:
            st.dataframe(
                due,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.success("No overdue follow-ups.")

    with right:
        st.markdown("#### Coming up in 7 days")
        st.caption(f"{len(upcoming)} upcoming reminders")

        if upcoming:
            st.dataframe(
                upcoming,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No upcoming follow-ups.")


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

elif page == "Statistics":

    st.markdown("#### Application performance")

    c1, c2, c3 = st.columns(3)
    c1.metric("Applications", total)
    c2.metric("Interviews", interviews)
    c3.metric("Offers", offers)

    counts = {
        status.title(): sum(
            1 for app in applications if app[2] == status
        )
        for status in VALID_STATUS
    }

    st.write("")

    if total:
        st.markdown("#### Applications by status")

        st.bar_chart(counts)

        response_rate = (
            (interviews + offers) / total * 100
        )

        st.markdown("#### Progress indicators")

        c1, c2 = st.columns(2)

        c1.metric(
            "Interview rate",
            f"{interviews / total * 100:.1f}%",
        )

        c2.metric(
            "Interview + offer rate",
            f"{response_rate:.1f}%",
        )

    else:
        st.info("Your analytics will appear after you add applications.")
