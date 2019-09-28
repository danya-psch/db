Лабораторна робота No 1. Ознайомлення з базовими операціями СУБД PostgreSQL
Завдання

Предметна галузь

Розроблення ігор(компанія розробник, гра, гравець, програміст)
Графічне представлення моделі

![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/diagram.png)

Структура бази даних
Структура таблиць бази даних

![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/database.png)

Опис структури бази даних


| Відношення  | Атрибути  |
|-------------|-----------|
|   Відношення "developer_company " <br> Вміщує інформацію про компанію розробника|   name – унікальна назва компанії(text)<br>date_of_birth – дата створення коппанії(date)|
|  Відношення "game "<br>Вміщує інформацію про гру що розробляється компанією |  age_restrictions – містить інформацію про вікові обмеження гри(int) <br>name – унікальна назва гри(text) <br>genre – жанр гри(text)|
| Відношення " player " <br>Вміщує інформацію про гравця, що грає в гру |  date_of_birth – дата народження гравця(date)<br>nickname – ім’я, яке гравець використовує у грі(text)<br> IP – унікальний ідентифікатор, який використовується для адресації комп’ютера в мережі(text)|
|  Відношення " programmer "<br>Вміщує інформацію про програміста, який працює в компанії  |  date_of_birth – дата народження програміста(date) <br>full_name – повне ім’я програміста(text) <br>salary – заробітна плата програміста(int) <br>experience – досвід роботі програміста в роках(real) <br>company – назва компанії в якій працює програміст(text)|

Вміст таблиць бази даних


Programmers<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/table___programmer.png)

Players<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/table___player.png)

Games<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/table___game.png)

Developer companies<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/table___developer_company.png)
