import os
import smtplib
from time import sleep
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(subject, message):
    toaddr = ['name@gmail.com', 'name@gmail.com'];
    fromaddr = 'name@gmail.com';
    mypass = "password";

    for toaddr in toaddr:
        msg = MIMEMultipart();
        msg['From'] = fromaddr;
        msg['To'] = toaddr;
        msg['Subject'] = subject;

        body = message;
        msg.attach(MIMEText(body, 'plain'));

        server = smtplib.SMTP('smtp.gmail.com', 587);
        server.starttls();
        server.login(fromaddr, mypass);
        text = msg.as_string();
        server.sendmail(fromaddr, toaddr, text);
        server.quit();

logs_files = {
    's1': {
        'path': '/logs/s1/access', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    's3': {
        'path': '/logs/s3/access', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    's6': {
        'path': '/logs/s6/access', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    's9': {
        'path': '/logs/s9/access', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    's11': {
        'path': '/logs/s11/access', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    'mx1': {
        'path': '/logs/mx1/mail.log', 'size_now': 0, 'size_old': 0, 'status': 0
    },
    'mx2': {
        'path': '/logs/mx2/mail.log', 'size_now': 0, 'size_old': 0, 'status': 0
    }
};

while True:
    for file in logs_files:
        if logs_files[file]['status'] == 0:
            logs_files[file]['size_old'] = os.path.getsize(logs_files[file]['path']);
            sleep(5.0);
            logs_files[file]['size_now'] = os.path.getsize(logs_files[file]['path']);
            if (logs_files[file]['size_old'] < logs_files[file]['size_now']):
                continue;
            else:
                logs_files[file]['status'] = 1;
                subject = 'Bad Events Log'
                send_mail(subject, "Перестала осуществляться запись данных в Лог " + logs_files[file]['path']);
        else:
            logs_files[file]['size_now'] = os.path.getsize(logs_files[file]['path']);
            if (logs_files[file]['size_old'] < logs_files[file]['size_now']):
                logs_files[file]['status'] = 0;
                subject = 'Good Events Log'
                send_mail(subject, "Данные вновь стали записываться в Лог " + logs_files[file]['path']);
            else:
                continue;
    if datetime.strftime(datetime.now(), "%H:%M") >= '23:45':
        sleep(1500);
    else:
        sleep(300);
