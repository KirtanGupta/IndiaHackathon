from __future__ import annotations

import csv
from itertools import product
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_emails.csv"

PHISHING_SENDERS = [
    "alerts@bank-secure.com",
    "support@wallet-check.com",
    "security@paypaI-alerts.com",
    "ops@company-support.net",
    "service@reward-center.biz",
    "mailer@shopper-win.net",
    "it-helpdesk@corp-mail.net",
    "admin@document-share.io",
    "notice@cloudverify.net",
    "billing@stream-renewal.com",
]

PHISHING_SUBJECTS = [
    "Verify your account now",
    "Account suspended notice",
    "Security alert on your profile",
    "Mailbox storage exceeded",
    "Claim your reward today",
    "Payroll access verification",
    "Reset your password immediately",
    "Unusual sign in attempt detected",
    "Invoice failed please confirm",
    "KYC update required today",
]

PHISHING_BODIES = [
    "Urgent action required to verify your password using the secure link below",
    "Your access will be suspended within 24 hours unless you confirm your login details now",
    "We detected unusual activity and need you to confirm your identity immediately",
    "Click the secure portal to avoid permanent account closure and restore service",
    "You have won a prize and must verify card details now to receive it",
    "Open the attached document and sign in to review the protected file",
    "Your payroll record is pending and requires employee credentials for release",
    "Update your banking profile now to remove the temporary suspension on your account",
    "Validate your mailbox password now or your messages will be deleted today",
    "Confirm your invoice information and login to prevent a service interruption",
]

BENIGN_SENDERS = [
    "team@example.com",
    "hr@example.com",
    "news@community.org",
    "finance@example.com",
    "support@saas.io",
    "noreply@travel.com",
    "teacher@college.edu",
    "alerts@weather.in",
    "admin@workspace.io",
    "events@localclub.org",
    "noreply@bank.com",
    "support@ecommerce.com",
    "finance@company.org",
    "it@office.local",
    "support@cloudapp.com",
]

BENIGN_SUBJECTS = [
    "Weekly project update",
    "Interview schedule for next week",
    "Monthly community newsletter",
    "Expense reimbursement processed",
    "Password changed confirmation",
    "Trip receipt attached",
    "Assignment reminder for Friday",
    "Weather advisory for tomorrow",
    "Workspace access summary",
    "Event registration confirmed",
    "Transaction alert",
    "Order delivered",
    "Payslip available",
    "Maintenance notice",
    "Invoice paid",
]

BENIGN_BODIES = [
    "Project notes for this week are attached for your review before the meeting",
    "Please find your interview schedule and venue details for next week",
    "Highlights from the community this month are included in this newsletter",
    "Your reimbursement has been processed successfully and will appear shortly",
    "This is a confirmation that your password was changed from account settings",
    "Your travel booking receipt is attached for your records and expense filing",
    "Submit the assignment by Friday evening using the course portal",
    "Rainfall warning in your district for tomorrow so plan travel accordingly",
    "Here is your workspace usage summary for the current billing cycle",
    "Your registration for the event has been confirmed and seats are reserved",
    "A debit card transaction of 550 INR was completed at City Mart",
    "Your package was delivered today and the invoice is available in the app",
    "Your payslip for March is available on the employee self-service portal",
    "VPN access may be intermittent tonight due to scheduled maintenance",
    "We received your subscription payment successfully and no further action is needed",
    "The bank statement for your account is ready to download from the portal",
    "Your refund request has been approved and will be credited within five business days",
    "This purchase confirmation includes the GST invoice for your completed order",
    "Your reimbursement request was approved by finance and is queued for transfer",
    "Scheduled maintenance will affect login for ten minutes after midnight tonight",
]


def build_rows(limit_per_label: int = 300) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for index, (sender, subject, body) in enumerate(
        product(PHISHING_SENDERS, PHISHING_SUBJECTS, PHISHING_BODIES)
    ):
        if index >= limit_per_label:
            break
        rows.append(
            {
                "sender": sender,
                "subject": subject,
                "body": body,
                "label": "phishing",
            }
        )

    for index, (sender, subject, body) in enumerate(
        product(BENIGN_SENDERS, BENIGN_SUBJECTS, BENIGN_BODIES)
    ):
        if index >= limit_per_label:
            break
        rows.append(
            {
                "sender": sender,
                "subject": subject,
                "body": body,
                "label": "benign",
            }
        )

    return rows


def write_dataset(rows: list[dict[str, str]]) -> Path:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["sender", "subject", "body", "label"])
        writer.writeheader()
        writer.writerows(rows)
    return DATA_PATH


if __name__ == "__main__":
    dataset_rows = build_rows(limit_per_label=300)
    path = write_dataset(dataset_rows)
    print(f"Wrote {len(dataset_rows)} rows to {path}")
