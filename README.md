<h1>Сервис по загрузке изображений с компьютера пользователя</h1>

# API методы для взаимодействия с сервисом
1. GET Получение списка доступных изображений: http://localhost:8000/api/images/
2. GET Получение детальной информации о изображении: http://localhost:8000/api/images/id/
3. POST Добавление изображений: http://localhost:8000/api/images/
   * BODY formdata {file или url}
4. POST Изменение размера изображения: http://localhost:8000/api/images/id/resize/
   * BODY formdata {width или height}
5. DELETE Удаление: http://localhost:8000/api/images/id/


# Настройка проекта
1. pip install -r requirements.txt 
2. python manage.py makemigrations 
3. python manage.py migrate 
4. python manage.py runserver

Все команды запускаются из главной директории с проектом