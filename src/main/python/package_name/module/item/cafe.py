# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
import threading
import json
import package_name.common.mail as mail
import yaml
import time
from package_name.common import config

reload(sys)
sys.setdefaultencoding('utf-8')

config.get_preference(config.EMAIL_CONF_PATH)
config_file = config.get_preference(config.CAFE_CONF_PATH)

used_cafe_url = 'http://cafe.naver.com/joonggonara'


def main(argv):
    mydriver = webdriver.Firefox()
    data = {}
    global config_file
    while True:
        with open(config_file, 'r') as stream:
            conf = yaml.load(stream)

        for keyword in conf.keys():
            key_conf = conf[keyword]
            select_notify(keyword, key_conf, data, mydriver)


def select_notify(keyword, conf, data, mydriver):
    fillter = conf['FILLTER']
    black_list = conf['BLACK_LIST']
    interval = conf['INTERVAL']
    print conf
    mydriver.get(used_cafe_url)
    input = "//input[@name='query']"
    btn = '//img[@class="btn-search-green"]'
    mydriver.find_element_by_xpath(input).send_keys(keyword)
    mydriver.find_element_by_xpath(btn).click()
    mydriver.switch_to.frame(mydriver.find_element_by_xpath("//iframe[@name='cafe_main']"))
    i = 0
    elements = get_board_list(i, mydriver)
    tmps = fillter_contents(black_list, data, elements, fillter, mydriver)
    if len(tmps) > 0:
        result_str = json.dumps(tmps, indent=4, ensure_ascii=False)
        result_str.replace("\n", "<BR>")
        config = mail.get_smtp_config()
        mail.send_mail(config, result_str)
    time.sleep(interval)


def fillter_contents(black_list, data, elements, fillter, mydriver):
    tmps = []
    for element in elements:
        black_bool = False
        for black in black_list:
            if black == element['author']:
                black_bool = True
        if black_bool:
            continue
        title_bool = False
        for word in fillter:
            if element['title'].find(word) > -1:
                title_bool = True
        if title_bool:
            continue
        if data.has_key(element['no']):
            pass
        else:
            contents = get_contents(element['href'], fillter, mydriver)
            data[element['no']] = contents
            if contents is None:
                pass
            else:
                tmps.append(element)
    return tmps


def get_board_list(i, mydriver):
    elements = []
    for element in mydriver.find_elements_by_xpath("//tr[@align='center']"):
        if i == 0:
            i = i + 1
            continue
        number = element.find_element_by_xpath(".//span[@class='m-tcol-c list-count']").text
        href = element.find_element_by_xpath(".//span[@class='aaa']/a").get_attribute('href')
        achor = element.find_element_by_xpath(".//span[@class='aaa']").text
        author = element.find_element_by_xpath(".//span[@class='wordbreak']").text
        create_time = element.find_element_by_xpath(".//td[@class='view-count m-tcol-c']").text
        result = {'no': number,
                  'href': href,
                  'title': achor,
                  'author': author,
                  'create_time': create_time}
        elements.append(result)
    return elements


def get_contents(link, fillter, mydriver):
    mydriver.get(link)
    #for iframe in mydriver.find_elements_by_xpath("//iframe"):
    #    mydriver.switch_to_frame(iframe)
    try:
        mydriver.switch_to.frame(mydriver.find_element_by_xpath("//iframe[@name='cafe_main']"))
        contents = mydriver.find_element_by_xpath("//div[@class='inbox']").text
    except BaseException, e:
        return None
    # contents = mydriver.find_element_by_xpath("//table[@class='comm-detail']").text
    # contents = contents + mydriver.find_element_by_xpath("//div[@class='NHN_Writeform_Main']").text
    for word in fillter:
        find_result = contents.find(word)
        if find_result > -1:
            return None
    return contents


def monitor_task_start():
    monitor_task = threading.Thread(target=main)
    monitor_task.setDaemon(True)
    monitor_task.start()

class MonitorTask(threading.Thread):
    def __init__(self, interval=600):
        threading.Thread.__init__(self, name='Monitor Task')
        self.interval = interval


if __name__ == "__main__":
    main(sys.argv[1:])
