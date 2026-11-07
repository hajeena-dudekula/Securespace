import sqlite3

connection = sqlite3.connect("instance/securespace.db")

admin = connection.execute(
    "SELECT username, role FROM secure_accounts WHERE username = ?",
    ("hajeenadudekula",)
).fetchone()

audit = connection.execute(
    "SELECT action FROM audit_logs ORDER BY id DESC LIMIT 1"
).fetchone()

print("Admin account:", admin)
print("Latest audit:", audit)

connection.close()
