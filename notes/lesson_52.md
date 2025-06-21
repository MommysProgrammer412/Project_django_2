# Тема Django. Переменные, теги условия и циклы шаблонизатора. Урок 52

## Экспериментальный шаблон 🧪

В прошлый раз мы бегло познакомились с шаблонизатором Django, включая переменные, условия и циклы.

Сейчас предлагаю углубится в эти темы.

### Создание шаблона 📝

Мы создадим тестовый шаблон, маршрут под него и представление.

Тестовый шаблон:
`test_template.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тестовый шаблон</title>
</head>
<body>
    <h1>Тестовый шаблон для опытов</h1>
    <h2>Комментарии HTML и шаблонизатора</h2>
    {% comment %} Это НЕ будет видно в браузере  {% endcomment %}
    <!-- Это будет видно в браузере -->
    <h2>Переменные шаблонизатора</h2>
    <p>{{ variable_1 }} - переменная Django</p>
    
</body>
</html>
```

Пояснения:

- `{% comment %} ... {% endcomment %}` - комментарий шаблонизатора
- `<!-- ... -->` - комментарий HTML - будет виден в браузере
- `{{ variable_1 }}` - переменная шаблонизатора, которую нужно передать из представления

Добавим маршрут в `urls.py`:

```python
from core.views import test_template
urlpatterns = [ ...
path("test_template/", test_template),
]
```

И представление:

```python
def test_template(request):
    """
    Отвечает за маршрут 'test_template/'
    """
    return render(request, "test_template.html")
```

### Проверяем работу разных типов данных

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_my_name(self):
        return f"Меня зовут {self.name}"
    
    def __str__(self):
        return f"Это метод __str__: {self.name}"

test_list = ["Алевтина", "Бородач", "Гендальф Серый", "Лысый из Игры Престолов"]
test_dict = {
    "master": "Алевтина",
    "age": 25,
    "is_master": True
}
test_person = Person("Лысый из Игры Престолов", 50)

def test_template(request):
    """
    Отвечает за маршрут 'test_template/'
    """
    
    context_data = {
        "variable_1": "Значение переменной 1",
        "test_list": test_list,
        "test_dict": test_dict,
        "test_person": test_person,
    }
    return render(request, "test_template.html", context=context_data)
```

И логика шаблона:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тестовый шаблон</title>
</head>
<body>
    <h1>Тестовый шаблон для опытов</h1>
    <h2>Комментарии HTML и шаблонизатора</h2>
    {% comment %} Это НЕ будет видно в браузере  {% endcomment %}
    <!-- Это будет видно в браузере -->
    <h2>Переменные шаблонизатора</h2>
        <p>{{ variable_1 }} - переменная Django</p>
    <h3>Список в шаблонизаторе</h3>
        <p> Весь список: {{ test_list }}</p>
        <p> Элемент 0: {{ test_list.0 }}</p>
        <p> Всего элементов в списке: {{ test_list|length }}</p>
    <h3>Словарь в шаблонизаторе</h3>
        <p> Весь словарь: {{ test_dict }}</p>
        <p> Значение по ключу "master": {{ test_dict.master }}</p>
        <p>Попробуем получить длину словаря: {{ test_dict|length }}</p>
    <h3>Объект в шаблонизаторе</h3>
        <p> Весь объект: {{ test_person }}</p>
        <p> Имя: {{ test_person.name }}</p>
        <p> Возраст: {{ test_person.age }}</p>
        <p> Вызов метода: {{ test_person.say_my_name }}</p>
    </body>
</html>
```

Пояснения:

- Про то как передаются разные типы данных и как они отображаются
- Про то что нельзя вызвать методы объекта с аргуменатми, только без аргументов


## Практическое применение циклов и условий шаблонизатора Django

### Подготовка спискового отображения заявок

`orders_list.html`
`path("orders/", orders_list),`


```python
def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    """
    context = {
        "orders": orders,
    }
    return render(request, "orders_list.html", context=context)
```

Переменная `data`:

```python
# Тестовые данные заявок
orders = [
    {
        "id": 1,
        "client_name": "Пётр 'Безголовый' Головин",
        "services": ["Стрижка под 'Горшок'", "Полировка лысины до блеска"],
        "master_id": 1,
        "date": "2025-03-20",
        "status": STATUS_NEW,
    },...
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список заявок</title>
    <style>
      
    </style>
</head>
<body>
    <h1>Список заявок</h1>
    <div class="flex-container">
        {% comment %} Проверка на пустую коллекцию empty{% endcomment %}
        {% for order in orders %}
        <div class="flex-card">
            <h2>ID заявки: {{ order.id }}</h2>
            <p>Имя: {{ order.client_name }}</p>
            
            <p>Дата заявки: {{ order.date }}</p>
            <p class= {% if order.status == "новая" %}
            "new"
            {% elif order.status == "подтвержденная" %}
            "confirmed"
            {% elif order.status == "отмененная" %}
            "rejected"
            {% elif order.status == "выполненная" %}
            "canceled"
            {% endif %}
            >Статус заявки: {{ order.status }}</p>
            <p>Количество услуг: {{ order.services|length }}</p>
            <div class="services">   
            {% comment %} цикл для span услуг {% endcomment %}
                {% for service  in order.services  %}
                <span class="service">{{ service }}</span>
                {% endfor %}
            </div> 

        </div>
        {% empty %}
        <p>Нет заявок</p>
        {% endfor %}

    </div>
</body>
</html>
```

-------------






## Фильтры шаблонизатора Django

| Название фильтра | Пример вызова | Пояснение |
|------------------|---------------|-----------|
| date             | `{{ value|date:"D d M Y" }}` | Форматирует дату в указанном формате. |
| upper            | `{{ value|upper }}` | Преобразует строку в верхний регистр. |
| lower            | `{{ value|lower }}` | Преобразует строку в нижний регистр. |
| slice            | `{{ some_list|slice:":2" }}` | Возвращает срез списка. |
| default          | `{{ value|default:"nothing" }}` | Возвращает значение по умолчанию, если значение не определено. |
| length           | `{{ some_list|length }}` | Возвращает длину списка или строки. |
| truncatechars    | `{{ value|truncatechars:10 }}` | Обрезает строку до указанного количества символов. |
| truncatewords    | `{{ value|truncatewords:2 }}` | Обрезает строку до указанного количества слов. |
| join             | `{{ list|join:", " }}` | Объединяет элементы списка в строку с указанным разделителем. |
| safe             | `{{ value|safe }}` | Помечает строку как безопасную для рендеринга HTML. |
| escape           | `{{ value|escape }}` | Экранирует HTML-теги в строке. |
| linebreaks       | `{{ value|linebreaks }}` | Заменяет переносы строк на теги `<br>`. |
| linebreaksbr     | `{{ value|linebreaksbr }}` | Заменяет переносы строк на теги `<br>`, сохраняя существующие теги `<br>`. |
| striptags        | `{{ value|striptags }}` | Удаляет все HTML-теги из строки. |
| add              | `{{ value|add:2 }}` | Прибавляет указанное число к значению. |
| divisibleby      | `{{ value|divisibleby:3 }}` | Проверяет, делится ли число на указанное значение без остатка. |
| yesno           | `{{ value|yesno:"yes,no,maybe" }}` | Возвращает одно из трех значений в зависимости от истинности значения. |
| filesizeformat  | `{{ value|filesizeformat }}` | Форматирует размер файла в удобочитаемом формате. |
| pluralize       | `{{ value|pluralize }}` | Возвращает множественное число слова в зависимости от значения. |
| time            | `{{ value|time:"H:i" }}` | Форматирует время в указанном формате. |
| timesince       | `{{ value|timesince:other_date }}` | Возвращает разницу во времени между двумя датами в удобочитаемом формате. |
| timeuntil       | `{{ value|timeuntil:other_date }}` | Возвращает время до указанной даты в удобочитаемом формате. |
| wordcount       | `{{ value|wordcount }}` | Возвращает количество слов в строке. |
| wordwrap        | `{{ value|wordwrap:10 }}` | Переносит строку по указанному количеству символов. |
| cut             | `{{ value|cut:" " }}` | Удаляет все вхождения указанной подстроки из строки. |
| first           | `{{ some_list|first }}` | Возвращает первый элемент списка. |
| last            | `{{ some_list|last }}` | Возвращает последний элемент списка. |
| random          | `{{ some_list|random }}` | Возвращает случайный элемент из списка. |
| floatformat     | `{{ value|floatformat:2 }}` | Форматирует число с плавающей точкой до указанного количества знаков после запятой. |
| get_digit       | `{{ value|get_digit:"2" }}` | Возвращает указанную цифру из числа. |
| make_list       | `{{ value|make_list }}` | Преобразует значение в список. |
| slugify         | `{{ value|slugify }}` | Преобразует строку в формат slug (только буквы, цифры, дефисы и подчеркивания). |
| stringformat    | `{{ value|stringformat:"s" }}` | Форматирует строку с использованием указанного формата. |
| urlencode       | `{{ value|urlencode }}` | Кодирует строку для использования в URL. |
| urlize          | `{{ value|urlize }}` | Преобразует URL-адреса в строке в кликабельные ссылки. |
| urlizetrunc     | `{{ value|urlizetrunc:20 }}` | Преобразует URL-адреса в строке в кликабельные ссылки и обрезает их до указанной длины. |
| capfirst         | `{{ value|capfirst }}` | Делает первую букву строки заглавной. |
| center           | `{{ value|center:"10" }}` | Центрирует строку в указанной ширине. |
| dictsort         | `{{ value|dictsort:"name" }}` | Сортирует список словарей по указанному ключу. |
| dictsortreversed | `{{ value|dictsortreversed:"name" }}` | Сортирует список словарей по указанному ключу в обратном порядке. |
| escapejs         | `{{ value|escapejs }}` | Экранирует JavaScript-код в строке. |
| fix_ampersands   | `{{ value|fix_ampersands }}` | Заменяет амперсанды на HTML-сущности. |
| iriencode        | `{{ value|iriencode }}` | Кодирует строку для использования в IRI. |
| linenumbers      | `{{ value|linenumbers }}` | Добавляет номера строк к тексту. |
| ljust            | `{{ value|ljust:"10" }}` | Выравнивает строку по левому краю в указанной ширине. |
| rjust            | `{{ value|rjust:"10" }}` | Выравнивает строку по правому краю в указанной ширине. |
| phone2numeric    | `{{ value|phone2numeric }}` | Преобразует телефонные номера в числовой формат. |
| removetags       | `{{ value|removetags:"b i" }}` | Удаляет указанные HTML-теги из строки. |
| title            | `{{ value|title }}` | Преобразует строку в формат заголовка (каждое слово с заглавной буквы). |
| unordered_list   | `{{ value|unordered_list }}` | Преобразует список в HTML-список без порядка. |
