# Урок: Работа с файлами в Python

## Сегмент 1: Основы работы с файлами

### theory
В Python для работы с файлами используются функции `open()`, `read()`, `write()`, `close()`.
Файлы открываются в режимах:
- `'r'` — чтение,
- `'w'` — запись (файл создаётся или перезаписывается),
- `'a'` — добавление в конец файла.

Пример открытия файла:
```python
with open('example.txt', 'r') as file:
    content = file.read()
```
### practice
Создайте файл test.txt и запишите в него строку "Hello, World!".
### answer
```python
with open('test.txt', 'w') as file:
    file.write("Hello, World!")
```

## Сегмент 2: Чтение и запись построчно
### theory
Для построчного чтения используйте цикл for line in file:.
Для записи списка строк используйте метод writelines().
        
### practice
Прочитайте файл test.txt и выведите каждую строку на экран.
### answer
```python
with open('test.txt', 'r') as file:
    for line in file:
        print(line.strip())
```