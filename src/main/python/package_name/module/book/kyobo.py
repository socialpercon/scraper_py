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
        mybook_url = "file:///D:/Dropbox/code/monaco/mybook.html"

        mydriver = webdriver.Chrome()
        print "start"
        mydriver.get(mybook_url)
        kyobo_url_list = ['http://used.kyobobook.co.kr/sellerPage/product/viewSellerProductList.ink?mmbrNmbr=62016023024']
        link_list = get_link_list(mydriver)
        print link_list
        for link in link_list:
            # link = u'http://book.naver.com/bookdb/book_detail.nhn?bid=7746778'
            try:
                isbn_list = []
                isbn_list.append(get_isbn(link, mydriver))
            except BaseException, e:
                print "failed, reason: {0}".format(repr(e))
        print isbn_list
        f_writer = open('./isbn_list','w')
        f_writer.write('\n'.join(isbn_list))
        exist_book_list = []
        for isbn in isbn_list:
            for kyobo_url in kyobo_url_list:
                exist_book_list.append(kyobo_url, get_exist_book(isbn, mydriver))

        print "end"
    except BaseException, e:
        print "login failed, reason: {0}".format(repr(e))

def get_kyobo(isbn_list, kyobo_url_list, mydriver):
    exist_book_list = []
    for isbn in isbn_list:
        for kyobo_url in kyobo_url_list:
            exist_book_list.append(get_exist_book(kyobo_url, isbn, mydriver))

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
