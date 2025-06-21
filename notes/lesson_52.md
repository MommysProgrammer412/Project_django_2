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
