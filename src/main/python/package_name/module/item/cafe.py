# -*- coding: utf-8 -*-
import sys
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

used_cafe_url = 'http://cafe.naver.com/joonggonara'


def main(argv):
    mydriver = webdriver.Firefox()
    mydriver.get(used_cafe_url)
    input = "//input[@name='query']"
    btn = '//img[@class="btn-search-green"]'
    keyword = u"노트 4"
    mydriver.find_element_by_xpath(input).send_keys(keyword)
    mydriver.find_element_by_xpath(btn).click()
    mydriver.switch_to.frame(mydriver.find_element_by_xpath("//iframe[@name='cafe_main']"))

    i = 0
    for element in mydriver.find_elements_by_xpath("//tr[@align='center']"):
        if i == 0:
            i = i + 1
            continue
        achor = element.find_element_by_xpath(".//span[@class='aaa']")
        result = {'no': element.find_element_by_xpath(".//span[@class='m-tcol-c list-count']").text,
                  'href': element.find_element_by_xpath(".//span[@class='aaa']/a").get_attribute('href'),
                  'title': achor.text,
                  'author': element.find_element_by_xpath(".//span[@class='wordbreak']").text,
                  'create_time': element.find_element_by_xpath(".//td[@class='view-count m-tcol-c']").text}
        print result
        # link = div.find_element_by_css_selector('a').get_attribute('href')
        # link_list.append(link)


if __name__ == "__main__":
    main(sys.argv[1:])
