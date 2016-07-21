# -*- coding: utf-8 -*-
from selenium import webdriver
from package_name.common import mail
import json


def test_get_smtp_config():
    config = mail.get_smtp_config()
    print config

def test_send_mail():
    mail.send_mail(mail.get_smtp_config(), "<br>".join(["{'a':1,'b':2,'c':3}", "{'1':'a'}"]))


if __name__ == "__main__":
    test_send_mail()