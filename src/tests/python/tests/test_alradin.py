# -*- coding: utf-8 -*-
from selenium import webdriver
from package_name.module.book import aladin

# def test_get_link_list():
#     mydriver = webdriver.Firefox()
#     naver.get_link_list(mydriver)


def test_alradin():
    mydriver = webdriver.Firefox()
    link = u'http://www.aladin.co.kr/usedstore/wstoremain.aspx?offcode=jamsil'
    book = {'title' : '아인슈타인', 'lowest' : '192931', 'isbn' : '9788901127217'}

    print aladin.alradin(link, book, mydriver)


if __name__ == "__main__":
    test_alradin()