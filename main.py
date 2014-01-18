# -*-coding: utf-8 -*-
from grab import Grab

g = Grab(log_file='f:/out.html')


def login():
    g.go('http://www.avito.ru/profile/login')
    g.set_input('login', 'epifanov.denis@gmail.com')
    g.set_input('password', 'secret')
    g.submit()


def get_old_items():
    result = []
    g.go('https://www.avito.ru/profile/items/old')
    for el in g.doc.select('//*[@id="overForm"]/div/div[2]/div').node_list():
        item = el.xpath('*/h3/a')[0]
        item_id = item.get('name')[5:]
        result.append((item_id, item.text))
    return result


def choice_items(items):
    selected_items = []
    show_all_old_items(items)
    choice_numbers = eval(raw_input('choice items: ') + ",")
    print 'you was choice:'
    print choice_numbers
    for number in choice_numbers:
        print items[number]
        selected_items.append(items[number])
    return selected_items


def show_all_old_items(items):
    for number, item in enumerate(items):
        print number, item[0], item[1]

login()
old_items = get_old_items()
for i in choice_items(old_items):
    print i[0], i[1]
