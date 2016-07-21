# -*- coding: utf-8 -*-

from package_name.module.item import cafe
from selenium import webdriver


def test_get_contents():
    link = "http://cafe.naver.com/ArticeRead.nhn?clubid=10050146&page=1&inCafeSearch=true&searchBy=1&query=%B3%EB%C6%AE+4&includeAll=&exclude=&include=&exact=&searchdate=all&media=0&sortBy=date&articleid=328418067&referrerAllArticles=true"
    link = "http://cafe.naver.com/joonggonara.cafe?iframe_url=/ArticleRead.nhn%3Fclubid=10050146%26page=1%26inCafeSearch=true%26searchBy=1%26query=%B3%EB%C6%AE+4%26includeAll=%26exclude=%26include=%26exact=%26searchdate=all%26media=0%26sortBy=date%26articleid=328470038%26referrerAllArticles=true"
    link = "http://cafe.naver.com/joonggonara.cafe?iframe_url=/ArticleRead.nhn%3Fclubid=10050146%26page=1%26inCafeSearch=true%26searchBy=1%26query=%B3%EB%C6%AE+4%26includeAll=%26exclude=%26include=%26exact=%26searchdate=all%26media=0%26sortBy=date%26articleid=328511667%26referrerAllArticles=true"
    mydriver = webdriver.Firefox()
    print cafe.get_contents(link, ['aaaaaa'], mydriver)


if __name__ == "__main__":
    test_get_contents()