## Проект "Recrutingsite"
## Командная разработка по методологии Agile:Scrum
## Сайт для поиска работы и найма сотрудников

### Базовая документация к проекту

Документация доступна после запуска приложения, по ссылке http://youdomain/admin/doc/

Основные системные требования:

* Python 3.8
* SQLite
* Django 3.1
* Зависимости (Python) из requirements.txt



#### получить проект можно из Git:
```
source /opt/venv/xabr/bin/activate
cd /opt/venv/xabr/src
git pull origin master
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic

```