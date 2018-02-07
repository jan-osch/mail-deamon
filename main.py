#!/usr/bin/env python3

import imaplib
import os
import threading
from time import sleep
from playsound import playsound
import yaml


def load_configuration():
    with open('./configuration.yaml', encoding='utf8') as file_pointer:
        return yaml.load(file_pointer)


def check_structure(schema, data):
    if isinstance(schema, tuple):  # tuple indicates alternative
        return any(map(lambda x: check_structure(x, data), schema))
    if isinstance(schema, list):
        return isinstance(data, list) and \
               all(map(lambda x: check_structure(schema[0], x), data))
    if isinstance(schema, dict):
        return isinstance(data, dict) and \
               all(map(lambda key: check_structure(schema.get(key), data.get(key)), schema.keys()))

    return isinstance(data, schema)


class Rule:
    def __init__(self, configuration):
        self.configuration = configuration
        self.memory = set()
        self.mail = None

    def start(self):
        self.log('rule starting')
        while True:
            self.execute()
            sleep(self.configuration['interval'])

    def log(self, message):
        print('Rule "{0}": {1}'.format(self.configuration['name'], message))

    def execute(self):
        self.log("executing rule")
        try:
            if self.mail is None:
                self.mail = self.connect_to_server()
            _, data = self.mail.search(None, self.configuration['condition'])
            self.check_ids(data[0].split())

        except Exception as error:
            self.log("executing failed reason: {0}".format(error))

    def connect_to_server(self):
        try:
            mail = imaplib.IMAP4_SSL(self.configuration['server'])
            mail.login(self.configuration['account'], self.configuration['password'])
            mail.select('inbox')
            self.log('successfully connected to {0}'.format(self.configuration['server']))
            return mail
        except imaplib.IMAP4.error as error:
            raise Exception("Cannot connect to {0} reason: {1}".format(self.configuration['server'], str(error)))

    def check_ids(self, ids):
        self.log('found: {0} matching emails'.format(len(ids)))
        for mail_id in ids:
            if mail_id not in self.memory:
                self.memory.add(mail_id)
                self.trigger()

    def trigger(self):
        for action in self.configuration['actions']:
            if 'sound' in action.keys():
                Rule.sound(action.get('sound'))
            if 'notify' in action.keys():
                Rule.notify('Mail Daemon', "Rule: " + self.configuration['name'], action.get('notify'))

    @staticmethod
    def notify(title, subtitle, message):
        formatted_title = '-title {!r}'.format(title)
        formatted_subtitle = '-subtitle {!r}'.format(subtitle)
        formatted_message = '-message {!r}'.format(message)
        os.system('terminal-notifier {}'.format(' '.join([formatted_message, formatted_title, formatted_subtitle])))

    @staticmethod
    def sound(file):
        playsound(file)


if __name__ == '__main__':
    configs = load_configuration()
    valid = check_structure([
        {
            'name': str,
            'server': str,
            'port': int,
            'account': str,
            'password': str,
            'condition': str,
            'interval': int,
            'actions': [
                ({'sound': str}, {'notify': str})
            ]
        }
    ], configs)
    if not valid:
        print("Configuration file invalid")
        exit(1)

    print("Successfully loaded {0} configs".format(len(configs)))
    for rule_config in configs:
        rule = Rule(rule_config)
        t = threading.Thread(target=rule.start)
        t.start()
