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

