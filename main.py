
import json
from datetime import datetime, date

FILE_NAME = "applications.json"

VALID_STATUS = [
    "applied",
    "interview",
    "offer",
    "rejected",
    "withdrawn"
]


# Load saved applications
try:
    with open(FILE_NAME, "r") as file:
        applications = json.load(file)

except FileNotFoundError:
    applications = []

except json.JSONDecodeError:
    print("Warning: Saved data file is empty or damaged.")
    applications = []


# Support records from the older version
for app in applications:
    while len(app) < 5:
        app.append("")


# Save applications
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(applications, file, indent=4)


# Get a non-empty value
def get_text(message):
    while True:
        value = input(message).strip()

        if value != "":
            return value

        print("This field cannot be empty.")


# Get a valid date
def get_date(message, allow_blank=False):
    while True:
        value = input(message).strip()

        if value == "" and allow_blank:
            return ""

        try:
            datetime.strptime(value, "%d-%m-%Y")
            return value

        except ValueError:
            print("Invalid date. Use DD-MM-YYYY, e.g. 30-10-2026.")


# Get a valid application status
def get_status():
    while True:
        print("Valid statuses:", ", ".join(VALID_STATUS))
        status = input("Enter status: ").strip().lower()

        if status in VALID_STATUS:
            return status

        print("Invalid status. Please try again.")


# Display one application
def show_application(app, num=None):
    if num is not None:
        print("\nApplication:", num)

    print("Company:", app[0])
    print("Role:", app[1])
    print("Status:", app[2])
    print("Application date:", app[3])
    print("Follow-up date:", app[4] or "Not set")


# Main program
while True:
    print("\n===== JOB APPLICATION TRACKER =====")
    print("1. Add application")
    print("2. View all applications")
    print("3. Update application status")
    print("4. Delete application")
    print("5. Search by company")
    print("6. View due follow-ups")
    print("7. View statistics")
    print("8. Exit")

    choice = input("Enter your choice: ").strip()

    # Add application
    if choice == "1":
        company = get_text("Enter company name: ")
        role = get_text("Enter job role: ")
        status = get_status()

        appl_date = get_date(
            "Application date (DD-MM-YYYY): "
        )

        follow_date = get_date(
            "Follow-up date (DD-MM-YYYY, or blank): ",
            allow_blank=True
        )

        # Ensure follow-up isn't before application date
        if follow_date != "":
            d1 = datetime.strptime(
                appl_date, "%d-%m-%Y"
            ).date()

            d2 = datetime.strptime(
                follow_date, "%d-%m-%Y"
            ).date()

            if d2 < d1:
                print("Follow-up cannot be before application date.")
                continue

        app = [
            company,
            role,
            status,
            appl_date,
            follow_date
        ]

        applications.append(app)
        save_data()

        print("Application added successfully!")

    # View all applications
    elif choice == "2":
        if not applications:
            print("No applications found.")
        else:
            for i, app in enumerate(applications, start=1):
                show_application(app, i)

    # Update application status
    elif choice == "3":
        if not applications:
            print("No applications to update.")
            continue

        for i, app in enumerate(applications, start=1):
            print(i, "-", app[0], "|", app[1], "|", app[2])

        try:
            num = int(input("Enter application number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if 1 <= num <= len(applications):
            applications[num - 1][2] = get_status()
            save_data()
            print("Status updated successfully!")
        else:
            print("Invalid application number.")

    # Delete application
    elif choice == "4":
        if not applications:
            print("No applications to delete.")
            continue

        for i, app in enumerate(applications, start=1):
            print(i, "-", app[0], "|", app[1])

        try:
            num = int(input("Enter application number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if 1 <= num <= len(applications):
            removed = applications.pop(num - 1)
            save_data()
            print("Deleted application for", removed[0])
        else:
            print("Invalid application number.")

    # Search by company
    elif choice == "5":
        search_name = get_text(
            "Enter company name to search: "
        ).lower()

        found = False

        for app in applications:
            if search_name in app[0].lower():
                show_application(app)
                found = True

        if not found:
            print("No matching applications found.")

    # View due follow-ups
    elif choice == "6":
        today = date.today()
        found = False

        for app in applications:
            if app[4] == "":
                continue

            try:
                follow_date = datetime.strptime(
                    app[4], "%d-%m-%Y"
                ).date()

            except ValueError:
                print("Invalid saved follow-up date for", app[0])
                continue

            if follow_date <= today:
                show_application(app)
                found = True

                if follow_date < today:
                    print("Reminder: Follow-up is overdue!")
                else:
                    print("Reminder: Follow-up is due today!")

        if not found:
            print("No follow-ups are due today or overdue.")

    # View statistics
    elif choice == "7":
        total = len(applications)

        print("\n===== APPLICATION STATISTICS =====")
        print("Total applications:", total)

        for status in VALID_STATUS:
            count = sum(
                1 for app in applications
                if app[2] == status
            )
            print(status.title() + ":", count)

        if total > 0:
            interviews = sum(
                1 for app in applications
                if app[2] == "interview"
            )

            offers = sum(
                1 for app in applications
                if app[2] == "offer"
            )

            print(
                "Interview rate:",
                round(interviews / total * 100, 1),
                "%"
            )

            print(
                "Offer rate:",
                round(offers / total * 100, 1),
                "%"
            )

    # Exit
    elif choice == "8":
        print("Tracker closed. Keep applying!")
        break

    else:
        print("Invalid choice. Enter a number from 1 to 8.")
