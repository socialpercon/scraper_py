# -*- coding: utf-8 -*-
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import argparse
import sys
import datetime
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import yaml
import os
import package_name.context as context


def main(argv):
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-rd', '--randomdelay', type=int, help='sleep randomly', default=1)
        parser.add_argument('-v', '--virtual', help='virtual browsing mode', action='store_true')

        args = parser.parse_args(argv)
        if args.virtual:
            print "virtual"
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1024, 768))
            display.start()
        delay_time = args.randomdelay
        rand_time = random.randrange(0, delay_time)
        print "delay time: {0}".format(rand_time)
        # time.sleep(rand_time)
        isbn_path = context.APPLICATION_HOME + '/src/tests/resources/isbn_list'
        print isbn_path
        f_read = open(isbn_path, 'r')

        isbn_list = []
        for line in f_read.readlines():
            isbn_list.append(line.replace("\n", ""))

        mydriver = webdriver.Firefox()
        aladin_url_format = "http://www.aladin.co.kr/usedstore/wstoremain.aspx?offcode=jamsil"
        print "start"
        for isbn in isbn_list:
            try:
                alradin(aladin_url_format, isbn, mydriver)
            except NoSuchElementException, e:
                pass
        # link_list = get_link_list(mydriver)
        exist_book_list = []

        print "end"
    except BaseException, e:
        print "login failed, reason: {0}".format(repr(e))


def alradin(aladin_url_format, isbn, mydriver):
    mydriver.get(aladin_url_format)
    input = "//input[@name='SearchWord']"
    btn = "//input[@class='searchBtn']"
    mydriver.find_element_by_xpath(input).send_keys(isbn)
    mydriver.find_element_by_xpath(btn).click()
    elements = []
    for element in mydriver.find_elements_by_xpath("//div[@class='ss_book_list']//ul"):
        elements.append(element.text.replace("\n", ""))

    if len(elements) >= 1:
        print "isbn : {0}".format(isbn), "#".join(elements)


def get_exist_book(kyobo_url, isbn, mydriver):
    mydriver.get(kyobo_url)
    input = "//input[@name='searchVal']"
    btn = "//p[@class='search']//a"
    el = mydriver.find_element_by_id('searchForm2')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'ISBN':
            option.click()  # select() in earlier versions of webdriver
            break
    mydriver.find_element_by_xpath(input).send_keys(isbn)
    mydriver.find_element_by_xpath(btn).click()
    for li in mydriver.find_elements_by_xpath("//ul[@class='list_type01']"):
        replace = li.text.replace('\n', '')
        print replace
        return replace


def get_link_list(mydriver):
    link_list = []
    for div in mydriver.find_elements_by_xpath("//div[@class='thumb_type']"):
        link = div.find_element_by_css_selector('a').get_attribute('href')
        print link
        link_list.append(link)
    return link_list


def get_isbn(link_tmp, mydriver):
    mydriver.get(link_tmp)
    element = mydriver.find_element_by_xpath("//div[@class='book_info_inner']")
    text_data = element.text.replace('\n', '')
    # pattern = ".*|ISBN 9(.*)|.*"
    pattern = ".*ISBN (.[0-9]+).*"
    compile_pattern = re.compile(pattern)
    isbn = compile_pattern.findall(text_data)
    return isbn[0]


if __name__ == "__main__":
    main(sys.argv[1:])
