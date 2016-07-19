# -*- coding: utf-8 -*-
import re

from selenium import webdriver
import argparse
import sys
import random
import package_name.context as context
import json
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool


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

        print "start"
        mydriver = webdriver.Firefox()
        link_list = get_link_list(mydriver)
        mydriver.close()
        link_path = context.APPLICATION_HOME + '/src/tests/resources/link_list'
        f_writer = open(link_path, 'w')
        f_writer.write(json.dumps(link_list))
        f_writer.close()

        # link_list = context.LINK_LIST
        write_to_file_book_info(link_list)
        print "end"
    except BaseException, e:
        print "login failed, reason: {0}".format(repr(e))


def write_to_file_book_info(link_list):
    isbn_list = []
    ebook_isbn_list = []
    event_num = 3
    import math
    max_int = int(math.ceil(float(len(link_list))/event_num))
    data_iter = []
    driver_pool = []
    pre_event_num = 0
    for i in xrange(1,event_num +1):
        cal_num = max_int/event_num + pre_event_num
        firefox = webdriver.Firefox()
        driver_pool.append(firefox)
        data_dict = {'links' : link_list[pre_event_num:cal_num], 'driver' : firefox}
        print data_dict
        pre_event_num = cal_num
        data_iter.append(data_dict)

    pool = Pool(event_num)
    book_infos = pool.map(get_books_info, data_iter)
    book_tmp = []
    for book_info_list in book_infos:
        book_tmp = book_tmp + book_info_list

    for book_info in book_tmp:
        if book_info['ebook']:
            ebook_isbn_list.append(book_info)
        else:
            isbn_list.append(book_info)
    isbn_path = context.APPLICATION_HOME + '/src/tests/resources/isbn_list'
    f_writer = open(isbn_path, 'w')
    f_writer.write(json.dumps(isbn_list))
    f_writer.close()
    ebook_isbn_path = context.APPLICATION_HOME + '/src/tests/resources/ebook_isbn_list'
    f_writer = open(ebook_isbn_path, 'w')
    f_writer.write(json.dumps(ebook_isbn_list))
    f_writer.close()
    for driver in driver_pool:
        driver.cloes()


def get_link_list(mydriver):
    mybook_url = context.MY_BOOK_URL
    mydriver.get(mybook_url)
    link_list = []
    for div in mydriver.find_elements_by_xpath("//div[@class='thumb_type']"):
        link = div.find_element_by_css_selector('a').get_attribute('href')
        link_list.append(link)
    return link_list

def get_books_info(data_dict):
    mydriver = data_dict['driver']
    link_list = data_dict['links']
    book_list = []
    for link in link_list:
        book_list.append(get_book_info(mydriver, link))

    return book_list

def get_book_info(mydriver, link):
    # element = mydriver.find_element_by_xpath("//div[@class='book_info_inner']")
    try:
        mydriver.get(link)
    except BaseException, e:
        print "cannot connect : {0}".format(link)
    book_info_dict = {}

    element = mydriver.find_element_by_xpath('//div[@class="book_info"]/h2')
    book_info_dict['title'] = element.text

    element = mydriver.find_element_by_xpath('//a[@id="txt_desc_point"]/strong')
    book_info_dict['score'] = element.text

    try:
        element = mydriver.find_element_by_xpath('//div[@class="lowest"]/strong')
        book_info_dict['lowest'] = element.text.replace(',', '')

        element = mydriver.find_element_by_xpath('//div[@class="lowest"]/span[@class="price"]')
        book_info_dict['normal'] = element.text.replace(',', '')
    except BaseException, e:
        element = mydriver.find_element_by_xpath('//div[@class="retail"]/strong')
        retail = element.text.replace(',', '')
        book_info_dict['normal'] = retail

    book_info_dict['isbn'] = get_isbn(mydriver)

    ebook_bool = False
    try:
        mydriver.find_element_by_xpath('//div[@class="ebook"]')
        ebook_bool = True
    except BaseException, e:
        pass
    book_info_dict['ebook'] = ebook_bool
    element = mydriver.find_element_by_xpath('//a[@id="txt_desc_point"]')
    href_value = element.get_attribute('href')
    book_info_dict['herf'] = href_value
    # pattern = ".*ISBN (.[0-9]+).*"
    # compile_pattern = re.compile(pattern)
    # isbn = compile_pattern.findall(text_data)
    return book_info_dict


# def get_isbn(book_info_dict, mydriver):
#     elements = mydriver.find_elements_by_xpath('//div[@class="book_info_inner"]/div')
#     element = elements[2]
#     origin_value = element.text
#     if len(origin_value) == 2:
#         page = origin_value.split('|')[0].split(' ')[1]
#         book_info_dict['page'] = page
#         isbn = origin_value.split('|')[1].split(' ')[1]
#         book_info_dict['isbn'] = isbn
#     elif len(origin_value) == 1:
#         isbn = origin_value.split('|')[0].split(' ')[1]
#         book_info_dict['isbn'] = isbn


def get_isbn(mydriver):
    element = mydriver.find_element_by_xpath("//div[@class='book_info_inner']")
    text_data = element.text.replace('\n', '')
    # pattern = ".*|ISBN 9(.*)|.*"
    pattern = ".*ISBN (.[0-9]+).*"
    compile_pattern = re.compile(pattern)
    isbn = compile_pattern.findall(text_data)
    return isbn[0]


if __name__ == "__main__":
    main(sys.argv[1:])
