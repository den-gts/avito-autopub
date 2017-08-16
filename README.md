avito-autopub
=============

Description
-----------
Avito sale Publication have expriration time (30 days). After expire that time you should go to avito.ru and click some links for republish your item offer. That service allow automate that republish.

Installation
------------

```bash
pip install .
```

Usage
-----

Just launch avitopub for interactive mode or pass command line arguments:

- a [Item id]  - Add item with [Item id] to autopub list. Item id you can find at interactive mode.
- r [Item id]  - remove item with [ITem id] from autopub list.
- p Apply autopub list. Subbmit changes at autopub list. Move items at active if item exist in autopub list. Move to finished avito list if doesn't exist at autopub list.

Russian description
-------------------
Объявления на avito.ru имеют ограниченный период жизни (30 дней). По истечению этого периода вам потребуется кликнуть по паре ссылок на сайте avito. Данных скрипт позволяет автоматизировать процесс продления объявления. Просто запустите скрипт, выберете объявления, которые требуется автопродлевать. Так же рекомендуется добавить команду python avitopub.py -p в ваш crontab или windows sсheduler для периодического автопродления.
