#!/usr/bin/env python3


import imaplib
from playsound import playsound
from time import sleep
import os
import email
from email.parser import HeaderParser

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "XXX" + ORG_EMAIL
FROM_PWD = "PAWSSWORD"
IMAP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

seen = set()


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)

    except imaplib.IMAP4.error as e:
        print('login failed')
        print(str(e))

    try:
        mail.select('inbox')
        # TODO implement rule set from https://tools.ietf.org/html/rfc3501#section-6.4.4
        type, data = mail.search(None, 'FROM quora SUBJECT bitcoin UNSEEN')
        mail_ids = data[0]

        id_list = mail_ids.split()
        print(id_list)
        played = False
        for elem in id_list:
            if elem not in seen:
                seen.add(elem)

                rv, data = mail.fetch(elem, 'BODY.PEEK[HEADER.FIELDS (SUBJECT)]')
                header_data = data[0][1]
                parser = HeaderParser()
                msg = parser.parsestr(header_data.decode('ascii'))

                do_notify()
                if not played:
                    do_song()
                    played = True

    except Exception as e:
        print(str(e))


def do_song():
    playsound("./completed.wav")


def do_notify():
    # Calling the function
    notify(title='New mail from jmgrzesik@gmail.com',
           subtitle='with python',
           message='New mail from jmgrzesik@gmail.com')


# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


if __name__ == '__main__':
    while True:
        read_email_from_gmail()
        sleep(30)
