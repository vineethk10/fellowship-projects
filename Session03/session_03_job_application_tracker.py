from datetime import datetime
import re

def get_non_empty_text(text_input):
    while True:
        user_input = input(text_input).strip()
        if user_input:
            return user_input
        print("[ERROR] Input cannot be empty. Try again.")

def get_valid_date(date_input):
    while True:
        try:
            user_input = input(date_input).strip()

            if user_input == "":
                raise ValueError("empty")

            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", user_input):
                raise ValueError("format")

            valid_date = datetime.strptime(user_input, "%Y-%m-%d").date()
            return valid_date

        except ValueError:
            print("[ERROR] Please enter a valid date in YYYY-MM-DD format, like 2026-04-08.")

def get_valid_status(status):
    valid_statuses = ["Applied", "Interview", "Offer", "Rejected", "Follow-Up Pending"]
    while True:
        status = input(status).strip().title()
        if status in valid_statuses:
            return status
        print(f"[ERROR] Status must be one of: {','.join(valid_statuses)}")

def create_application(company, role, applied_date, status):
    return {
        "company": company,
        "role": role,
        "date_applied": applied_date,
        "status": status
    }

def count_by_status(applications, target_status):
    return sum(1 for app in applications if app["status"] == target_status)


def get_pending_followups(applications):
    return [app for app in applications if app["status"] == "Follow-Up Pending"]


def print_application_summary(applications):
    print("\n=== Job Application Pipeline Summary ===")

    if not applications:
        print("[RESULT] No applications logged yet.")
        return

    print(f"Total Applications: {len(applications)}")
    print(f"Applied: {count_by_status(applications, 'Applied')}")
    print(f"Interview: {count_by_status(applications, 'Interview')}")
    print(f"Offer: {count_by_status(applications, 'Offer')}")
    print(f"Rejected: {count_by_status(applications, 'Rejected')}")
    print(f"Follow-Up Pending: {count_by_status(applications, 'Follow-Up Pending')}")

    pending = get_pending_followups(applications)
    print("\nPending Follow-Ups:")
    if pending:
        for app in pending:
            print(
                f"- {app['company']} | {app['role']} | Applied on {app['date_applied']}"
            )
    else:
        print("None")

    print("\nAll Applications:")
    for index, app in enumerate(applications, start=1):
        print(
            f"{index}. Company: {app['company']}, "
            f"Role: {app['role']}, "
            f"Date Applied: {app['date_applied']}, "
            f"Status: {app['status']}"
        )

def main():
    applications = []
    print("=== Job Application Tracker ===")

    while True:
        print("\nChoose an option:")
        print("1. Add application")
        print("2. Show summary")
        print("3. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            company = get_non_empty_text("Enter company name: ")
            role = get_non_empty_text("Enter job role: ")
            applied_date = get_non_empty_text("Enter date applied (YYYY-MM-DD): ")

            status = get_valid_status("Enter status (Applied, Interview, Offer, Rejected, Follow-Up Pending): " )

            application = create_application(company, role, applied_date,status)
            applications.append(application)
            print("[RESULT] Application added successfully.")
        elif choice == "2":
            print_application_summary(applications)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("[ERROR] Invalid choice. Please enter 1,2, or 3.")


if __name__ == '__main__':
    main()