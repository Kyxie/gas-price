import os
import requests
import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from model.Contants import Constants
from datetime import datetime
from model.Info import Info


SPLITER = "\n" + "-" * 45 + "\n"


def gas_price(user):
    target = Constants.TARGET + user.city
    if config.fetch_new:
        try:
            response = requests.get(url=target)
            response.raise_for_status()
            with open(Constants.TXT_FILE, "w", encoding="utf-8") as f:
                f.write(response.text)
        except:
            print("Request Error")
            exit(1)

    with open(Constants.TXT_FILE, "r", encoding="utf-8") as f:
        line = f.readline()
        info_list = []
        while line:
            line = Constants.pattern_parser(Constants.START_PATTERN, line, Constants.LINE)
            if line is not None:
                days = Constants.pattern_parser(Constants.DAY_PATTERN, line, Constants.ALL)
                dates = Constants.pattern_parser(Constants.DATE_PATTERN, line, Constants.ALL)
                regus = Constants.pattern_parser(Constants.REGU_PATTERN, line, Constants.ALL)
                prems = Constants.pattern_parser(Constants.PREM_PATTERN, line, Constants.ALL)
                info_list = [
                    Info(day, date, regu[0], regu[1], prem[0], prem[1])
                    for day, date, regu, prem in zip(days, dates, regus, prems)
                ]
                info_list.sort(key=lambda x: datetime.strptime(x.date, "%b %d, %Y"))
                break
            line = f.readline()

    if config.delete_text:
        os.remove(Constants.TXT_FILE)

    res = ""
    today = datetime.now()
    today_date = today.strftime("%b %d, %Y").replace(" 0", " ")
    tomorrow = today + timedelta(days=1)
    tomorrow_date = tomorrow.strftime("%b %d, %Y").replace(" 0", " ")
    res += f"Hi {user.name}, here is the gas report in {user.city}"
    res += SPLITER
    for info in info_list:
        if info.date == today_date:
            res += f"Date: {info.date} ({info.day}) - Today\n"
        elif info.date == tomorrow_date:
            res += f"Date: {info.date} ({info.day}) - Tomorrow\n"
        else:
            res += f"Date: {info.date} ({info.day})\n"
        res += f"  Regular Price: {info.regu}, Change: {info.regu_change}\n"
        res += f"  Premium Price: {info.prem}, Change: {info.prem_change}\n\n"

    res = res.strip()
    res += SPLITER
    res += f"Report generated on {today_date}\n"
    res += f"Source: {Constants.TARGET}{user.city}"
    return res


def send_email(mail_to, content):
    username = config.username
    password = config.password
    mail_from = username
    mail_subject = "Gas Price Tomorrow"
    mail_body = content
    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Subject"] = mail_subject
    msg.attach(MIMEText(mail_body, "plain"))
    connection = smtplib.SMTP(host=config.host, port=config.port)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(msg)
    connection.quit()


def main():
    # Recipient configuration
    users = config.users

    for user in users:
        content = gas_price(user=user)
        print(content)
        if config.send_email:
            if user.subscribe:
                send_email(mail_to=user.email, content=content)


if __name__ == "__main__":
    main()
