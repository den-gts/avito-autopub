# -*-coding: utf-8 -*-
from grab import Grab, GrabError, DataNotFound

g = Grab()


def login():
    g.go('http://www.avito.ru/profile/login')
    g.set_input('login', 'epifanov.denis@gmail.com')
    g.set_input('password', 'secret')
    g.submit()
    try:
        if g.doc.select('/html/body/div[1]/div[2]/div/div/h2').text() == u'Вход':
            raise GrabError('Wrong login/password')
    except DataNotFound:
        pass


def get_items(itemtype):
    """get items from profile.
    itemtype: 'old' for old items. 'active' for active items"""
    result = []
    g.go('https://www.avito.ru/profile/items/%s' % itemtype)
    for el in g.doc.select('//*[@id="overForm"]/div/div[2]/*/div[@class="description"]').node_list():
        item = el.xpath('h3/a')[0]
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
        print items[number][1]
        selected_items.append(items[number])
    return selected_items


def show_all_old_items(items):
    for number, item in enumerate(items):
        print "%d)(%s) %s" % (number, item[0], item[1])


def ids_form_settings():
    try:
        with open('settings.cfg', 'r') as settings:
            exist_id = settings.readlines()
            return map(lambda x: str(int(x)), exist_id)
    except IOError:
        return []


def save_ids(exist_ids):
    exist_ids = [x + '\n' for x in exist_ids]
    with open('settings.cfg', 'w') as settings:
        settings.writelines(exist_ids)


def add_to_autopub():
    old_items = get_items('old')
    active_items = get_items('active')
    selected = choice_items(active_items+old_items)
    exist_id = ids_form_settings()
    for item in selected:
        if (item[0]) not in exist_id:
            exist_id.append(item[0])
    save_ids(exist_id)


def items_from_settings():
    ids = ids_form_settings()
    all_web_items = get_items('active') + get_items('old')
    return filter(lambda item: item[0] in ids, all_web_items)


def remove_from_setting(item_id):
    exists_id = ids_form_settings()
    exists_id.remove(str(item_id))
    save_ids(exists_id)


def select_to_remove():
    print "Choice item for remove from autopub list:"
    for number, item in enumerate(items_from_settings(), 1):
        print "%d)(%s) %s" % (number, item[0], item[1])

login()
select_to_remove()