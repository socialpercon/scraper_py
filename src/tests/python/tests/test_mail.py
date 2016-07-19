# -*- coding: utf-8 -*-
from selenium import webdriver
from package_name.common import mail


def test_get_smtp_config():
    config = mail.get_smtp_config()
    print config


if __name__ == "__main__":
    test_get_smtp_config()