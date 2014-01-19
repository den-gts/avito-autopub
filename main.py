# -*-coding: utf-8 -*-
from grab import Grab, GrabError, DataNotFound
import sys
import argparse
parser = argparse.ArgumentParser(prog="AVITO autopublisher")
g = Grab()


def login():
    """login to avito.ru. Login and password will get from login.cfg.
    format login.cfg: first row - login, second - password.
    etc:
    admin@admin.ru
    megapassword
    """
    with open('login.cfg') as logincfg:
        logindata = logincfg.readlines()
    g.go('http://www.avito.ru/profile/login')
    g.set_input('login', logindata[0])
    g.set_input('password', logindata[1])
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
    """promt user for choice item or items. always return list of items"""
    selected_items = []
    print_items(items)
    try:
        choice_numbers = eval(raw_input('choice items: ') + ",")
    except StandardError:
        print 'invalid choice number'
        return choice_items(items)
    if choice_numbers == 0:
        return main_loop()
    print 'you was choice:'
    try:
        for number in choice_numbers:
            print items[number][1]
            selected_items.append(items[number - 1])
        return selected_items
    except IndexError:
        print 'invalid choice number'
        choice_items(items)


def print_items(items):
    """print items for choise etc."""
    teamplate = "%d)(%s) %s"
    for number, item in enumerate(items, 1):
        print teamplate % (number, item[0], item[1])


def ids_form_settings():
    """get items ids from file settings.cfg"""
    try:
        with open('settings.cfg', 'r') as settings:
            exist_id = settings.readlines()
            return map(lambda x: str(int(x)), exist_id)
    except IOError:
        return []


def save_ids(exist_ids):
    """save items ids to file settings.cfg"""
    exist_ids = [x + '\n' for x in exist_ids]
    with open('settings.cfg', 'w') as settings:
        settings.writelines(exist_ids)


def add_to_settings(items_id):
    exist_id = ids_form_settings()
    for item in items_id:
        if (item[0]) not in exist_id:
            exist_id.append(item[0])
    save_ids(exist_id)


def check_id(item_id):
    web_id = [x[0] for x in (get_items('old') + get_items('active'))]
    if item_id not in web_id:
        return False
    return True


def add_to_autopub():
    """show all items, promt for adding to autopub list in setting.cfg"""
    old_items = get_items('old')
    active_items = get_items('active')
    print "0) exit"
    print "choise item for adding to autopub list:"
    selected = choice_items(active_items+old_items)
    add_to_settings(selected)


def items_from_settings():
    """return items from autopub list in settings.cfg file"""
    ids = ids_form_settings()
    all_web_items = get_items('active') + get_items('old')
    return filter(lambda item: item[0] in ids, all_web_items)


def remove_from_setting(items_id):
    """remove item by id from autopub list in setting.cfg"""
    exists_id = ids_form_settings()
    for item_id in items_id:
        try:
            exists_id.remove(item_id)
        except ValueError:
            return
    save_ids(exists_id)
    return True


def select_to_remove():
    """show items from autopub list, promt for removing from list and remove selected items ids"""
    print "Choice item for remove from autopub list:"
    settings_items = items_from_settings()
    print "0) exit"
    selected = choice_items(settings_items)
    remove_from_setting([x[0] for x in selected])


def apply_autopub():
    settings_ids = ids_form_settings()
    web_old_ids = [item[0] for item in get_items('old')]
    for id_item in settings_ids:
        if id_item in web_old_ids:
            g.go('https://www.avito.ru/profile/items/old?item_id[]=%s&start' % id_item)
            print "adding item with id '%s' to active list" % id_item


def main_loop():
    print "="*40
    print "autopub list:"
    print_items(items_from_settings())
    print "="*40
    actions = {'add': add_to_autopub,
           'remove': select_to_remove,
           'apply': apply_autopub,
           'exit': sys.exit}
    actions_order = ['add', 'remove', 'apply', 'exit']
    actions_num_list = tuple(enumerate(actions_order, 1))
    for number, action in actions_num_list:
        print "%d) %s" % (number, action)
    try:
        choice = int(raw_input('choice action:'))
        if not (1 <= choice <= len(actions_order)):
            raise ValueError
    except ValueError:
        print "invalid action number"
    else:
        actions[actions_num_list[choice-1][1]]()

    main_loop()

if len(sys.argv) == 1:
    main_loop()
else:
    parser.add_argument("-p", "--apply", dest="apply", action='store_true', help="apply autopub list")
    parser.add_argument("-a", "--add", dest='ids_to_add', action='store', default=[], nargs="+",
                        help='add ids to autopub list')
    parser.add_argument("-r", "--remove", dest='ids_to_remove', action='store', default=[], nargs="+",
                        help='remove ids from autopub list')
    namespace = parser.parse_args(sys.argv[1:])
    for item_id in namespace.ids_to_add + namespace.ids_to_remove:
        if not item_id.isdigit():
            print 'ERROR: invalid id "%s"' % item_id
            sys.exit(1)
    checked_ids = []
    login()
    for item_id in namespace.ids_to_add:
        if check_id(item_id):
            checked_ids.append(item_id)
        else:
            print "id '%s' dont exist in avito" % item_id

    add_to_settings(checked_ids)
    remove_from_setting(namespace.ids_to_remove)

