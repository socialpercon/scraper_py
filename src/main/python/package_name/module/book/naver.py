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

        mydriver = webdriver.Firefox()
        print "start"
        kyobo_url_list = ['http://used.kyobobook.co.kr/sellerPage/product/viewSellerProductList.ink?mmbrNmbr=12002582007']
        # link_list = get_link_list(mydriver)
        write_to_file_book_info(mydriver)
        print "end"
    except BaseException, e:
        print "login failed, reason: {0}".format(repr(e))


def write_to_file_book_info(mydriver, link_list):
    isbn_list = []
    ebook_isbn_list = []
    for link in link_list:
        # link = u'http://book.naver.com/bookdb/book_detail.nhn?bid=7746778'
        try:
            book_info = get_book_info(link, mydriver)
            if book_info[1]:
                ebook_isbn_list.append(book_info[0])
            else:
                isbn_list.append(book_info[0])
        except BaseException, e:
            print "failed, reason: {0}".format(repr(e))
    f_writer = open('./isbn_list', 'w')
    f_writer.write('\n'.join(isbn_list))
    f_writer.close()
    f_writer = open('./ebook_isbn_list', 'w')
    f_writer.write('\n'.join(ebook_isbn_list))
    f_writer.close()


def get_link_list(mydriver):
    mybook_url = context.MY_BOOK_URL
    mydriver.get(mybook_url)
    link_list = []
    for div in mydriver.find_elements_by_xpath("//div[@class='thumb_type']"):
        link = div.find_element_by_css_selector('a').get_attribute('href')
        link_list.append(link)
    return link_list


def get_book_info(link_tmp, mydriver):
    mydriver.get(link_tmp)
    element = mydriver.find_element_by_xpath("//div[@class='book_info_inner']")
    text_data = element.text.replace('\n', '')
    is_ebook = text_data.find("ebook") > -1
    # pattern = ".*|ISBN 9(.*)|.*"
    pattern = ".*ISBN (.[0-9]+).*"
    compile_pattern = re.compile(pattern)
    isbn = compile_pattern.findall(text_data)
    return (isbn[0], is_ebook)

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
