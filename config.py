from model.User import User

# General configuration
fetch_new = True
send_email = False
delete_text = True

# SMTP configuration
username = "sender@gmail.com"
password = "password"
host = "smtp.gmail.com"
port = 587

users = [
    User("Kyxie", "Toronto", "recipient@outlook.com", True),
    User("Lawrence", "Vancouver", "recipient@outlook.com", False)
]