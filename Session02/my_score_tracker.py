print("Welcome to the Job Application Score Tracker!")
collected_inputs = []

# for i in range(3):
#     count = i+1
#     print("\n" + "=" * 80)
#     company_name = input(f"Application {count} - Enter company name: ")
#     job_role = input(f"Application {count} - Enter job role: ")
#     app_status = input(f"Application {count} - Enter status (Applied/Pending/Rejected/Accepted): ")
#     application = {
#         "company": company_name,
#         "role": job_role,
#         "status": app_status
#     }
#     collected_inputs.append(application)

count = 0
while count < 3:
    count = count+1
    print("\n" + "=" * 80)
    company_name = input(f"Application {count} - Enter company name: ")
    job_role = input(f"Application {count} - Enter job role: ")
    app_status = input(f"Application {count} - Enter status (Applied/Pending/Rejected/Accepted): ")
    application = {
        "company": company_name,
        "role": job_role,
        "status": app_status
    }
    collected_inputs.append(application)

print("\n" + "=" * 80)

print("Your Job Applications:")

if len(collected_inputs) == 3:
    print("You have collected 3 applications - ready to process!")
elif len(collected_inputs) > 3:
    print(f"You have collected {len(collected_inputs)} applications")
else:
    print(f"You have collected {len(collected_inputs)} applications. Missing {3-len(collected_inputs)} to complete.")

print("\n" + "=" * 80)

active_applications = [app for app in collected_inputs if app['status'] in ['Applied', 'Pending']]

print("Applications that need follow up.")

if active_applications:
    for idx, app in enumerate(active_applications, start=1):
        print(f" {idx}. {app['company']} - {app['role']} (Status: {app['status']})")
else:
    print(" You have no applications to follow up ")
    
print("\n" + "=" * 80)