
import json
import streamlit as st
from datetime import datetime, date

FILE_NAME = "applications.json"

VALID_STATUS = [
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn"
]


def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            apps = json.load(file)

        for app in apps:
            while len(app) < 5:
                app.append("")

        return apps

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        st.error("The saved data file is invalid.")
        return []


def save_data(apps):
    with open(FILE_NAME, "w") as file:
        json.dump(apps, file, indent=4)


st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Job Application Tracker")
st.write("Track your applications, statuses, and follow-ups.")

applications = load_data()

# Dashboard statistics
total = len(applications)
interviews = sum(1 for app in applications if app[2] == "interview")
offers = sum(1 for app in applications if app[2] == "offer")
rejected = sum(1 for app in applications if app[2] == "rejected")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Applications", total)
c2.metric("Interviews", interviews)
c3.metric("Offers", offers)
c4.metric("Rejected", rejected)

st.divider()

# Add application
st.subheader("➕ Add Application")

with st.form("add_application"):
    company = st.text_input("Company name")
    role = st.text_input("Job role")

    status = st.selectbox(
        "Application status",
        VALID_STATUS
    )

    appl_date = st.date_input(
        "Application date",
        value=date.today()
    )

    follow_date = st.date_input(
        "Follow-up date (optional)",
        value=None
    )

    submitted = st.form_submit_button("Save Application")

    if submitted:
        if not company.strip() or not role.strip():
            st.error("Company name and job role are required.")

        elif follow_date is not None and follow_date < appl_date:
            st.error("Follow-up date cannot be before application date.")

        else:
            follow_text = (
                follow_date.strftime("%d-%m-%Y")
                if follow_date is not None
                else ""
            )

            applications.append([
                company.strip(),
                role.strip(),
                status,
                appl_date.strftime("%d-%m-%Y"),
                follow_text
            ])

            save_data(applications)
            st.success("Application saved!")
            st.rerun()

st.divider()

# View applications
st.subheader("📋 Your Applications")

if applications:
    search = st.text_input("Search by company")
    status_filter = st.selectbox(
        "Filter by status",
        ["all"] + VALID_STATUS
    )

    filtered = [
        app for app in applications
        if search.lower() in app[0].lower()
    ]

    rows = []

    for i, app in enumerate(applications):
        if (
                search.lower() in app[0].lower()
                and (status_filter == "all" or app[2] == status_filter)
        ):
            rows.append({
                "Company": app[0],
                "Role": app[1],
                "Status": app[2].title(),
                "Application Date": app[3],
                "Follow-up Date": app[4] or "Not set"
            })

    st.dataframe(rows, use_container_width=True)

    # Update status
    st.subheader("✏️ Update Status")

    company_options = [
        f"{i + 1}. {app[0]} — {app[1]}"
        for i, app in enumerate(applications)
    ]

    selected = st.selectbox(
        "Choose an application",
        company_options
    )

    index = company_options.index(selected)

    new_status = st.selectbox(
        "New status",
        VALID_STATUS,
        key="new_status"
    )

    if st.button("Update Status"):
        applications[index][2] = new_status
        save_data(applications)
        st.success("Status updated!")
        st.rerun()

    # Delete application
    st.subheader("🗑️ Delete Application")

    delete_choice = st.selectbox(
        "Choose application to delete",
        company_options,
        key="delete_choice"
    )

    if st.button("Delete Application"):
        delete_index = company_options.index(delete_choice)
        deleted = applications.pop(delete_index)
        save_data(applications)
        st.success(f"Deleted {deleted[0]}.")
        st.rerun()

else:
    st.info("No applications yet. Add your first application above.")

st.divider()

# Due follow-ups
st.subheader("⏰ Due Follow-ups")

today = date.today()
due = []

for app in applications:
    if app[4] == "":
        continue

    try:
        follow = datetime.strptime(
            app[4], "%d-%m-%Y"
        ).date()

        if follow <= today:
            due.append({
                "Company": app[0],
                "Role": app[1],
                "Follow-up Date": app[4],
                "Reminder": "Overdue" if follow < today else "Due today"
            })

    except ValueError:
        pass

if due:
    st.dataframe(due, use_container_width=True)
else:
    st.write("No follow-ups due today or overdue.")
