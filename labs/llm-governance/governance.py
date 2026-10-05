import pandas as pd
from datetime import datetime


USERS_FILE = "users.csv"
AUDIT_FILE = "audit_log.csv"


print("Starting LLM governance workflow...")


# Load users and roles
users_df = pd.read_csv(USERS_FILE)


# Define permissions for each role
permissions = {
    "Admin": [
        "update_model",
        "run_model",
        "view_results"
    ],
    "Developer": [
        "run_model",
        "view_results"
    ],
    "Viewer": [
        "view_results"
    ]
}


# Sample governance requests
requests = [
    {
        "user": "Alice",
        "action": "update_model"
    },
    {
        "user": "Bob",
        "action": "run_model"
    },
    {
        "user": "Carol",
        "action": "run_model"
    },
    {
        "user": "David",
        "action": "view_results"
    }
]


audit_records = []


# Evaluate each request
for request in requests:

    user = request["user"]
    action = request["action"]

    user_record = users_df[
        users_df["user"] == user
    ]

    if user_record.empty:

        role = "Unknown"
        decision = "DENIED"

    else:

        role = user_record.iloc[0]["role"]

        allowed_actions = permissions.get(
            role,
            []
        )

        if action in allowed_actions:
            decision = "ALLOWED"
        else:
            decision = "DENIED"


    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )


    audit_records.append({
        "timestamp": timestamp,
        "user": user,
        "role": role,
        "action": action,
        "decision": decision
    })


    print()
    print(f"User: {user}")
    print(f"Role: {role}")
    print(f"Action: {action}")
    print(f"Decision: {decision}")


# Create audit log dataframe
audit_df = pd.DataFrame(
    audit_records
)


# Save audit log
audit_df.to_csv(
    AUDIT_FILE,
    index=False
)


# Calculate summary
total_requests = len(audit_df)

allowed_requests = (
    audit_df["decision"] == "ALLOWED"
).sum()

denied_requests = (
    audit_df["decision"] == "DENIED"
).sum()


print()
print("Governance Summary")
print("------------------")

print(
    f"Total Requests: "
    f"{total_requests}"
)

print(
    f"Allowed Requests: "
    f"{allowed_requests}"
)

print(
    f"Denied Requests: "
    f"{denied_requests}"
)

print()
print(
    f"Audit log saved to: "
    f"{AUDIT_FILE}"
)

print(
    "Governance workflow "
    "completed successfully."
)