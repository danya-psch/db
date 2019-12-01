h1 Лабораторна робота No 2. Ознайомлення з базовими операціями СУБД PostgreSQL
=====================

h2 Варіант завданн
-----------------------------------
15 варінт згідно номема у списку

| Пошук за атрибутами | Повнотекстовий пошук  |
|-------------|-----------|
| Діапазон чисел, перелічення | Обов’язкове входження слова, ціла фраза|

h2 Нормалізована модель даних
-----------------------------------
У порівнянні з попередньої лабораторною роботою, до таблиць game, programmer, player, developer_company були добавлені поля id, які стали единими первинними ключами відношень. До відношення developer_company був добвлений атрибут description.

Розроблення ігор(компанія розробник, гра, гравець, програміст)
Графічне представлення моделі

![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/diagram.png)

Структура бази даних
Структура таблиць бази даних

![](https://github.com/DanyaPes/db/blob/master/sem5/lab1/img/database.png)

Опис структури бази даних


| Відношення  | Атрибути  |
|-------------|-----------|
| Відношення "developer_company " <br> Вміщує інформацію про компанію розробника|   id - ідентифікатор компанії(integer)<br>name – унікальна назва компанії(text)<br>date_of_birth – дата створення коппанії(date)|
| Відношення "game__player" <br> Вміщує інформацію про відношення гравця до ігор|   id - ідентифікатор гравця(integer)<br>, game_id – ідентифікатор гри(text)|
| Відношення "developer_company__game" <br> Вміщує інформацію про відношення компанії розробника до ігор, які були нею розроблені| developer_company_id - ідентифікатор компанії(integer)<br>game_id - ідентифікатор гри(integer)<br>release_date - дата випуску гри(date)|
| Відношення "game "<br>Вміщує інформацію про гру що розробляється компанією |  id - ідентифікатор гри(integer)<br>age_restrictions – містить інформацію про вікові обмеження гри(int) <br>name – унікальна назва гри(text) <br>genre – жанр гри(text)|
| Відношення " player " <br>Вміщує інформацію про гравця, що грає в гру |  id - ідентифікатор гравця(integer)<br>date_of_birth – дата народження гравця(date)<br>nickname – ім’я, яке гравець використовує у грі(text)<br> IP – унікальний ідентифікатор, який використовується для адресації комп’ютера в мережі(text)|
| Відношення " programmer "<br>Вміщує інформацію про програміста, який працює в компанії  |  id - ідентифікатор програміста(integer)<br>date_of_birth – дата народження програміста(date) <br>full_name – повне ім’я програміста(text) <br>salary – заробітна плата програміста(int) <br>experience – досвід роботі програміста в роках(real) <br>company – назва компанії в якій працює програміст(text)|

Вміст таблиць бази даних


Programmers<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab2/img/table___programmer.png)

Players<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab2/img/table___player.png)

Games<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab2/img/table___game.png)

Developer companies<br>
![](https://github.com/DanyaPes/db/blob/master/sem5/lab2/img/table___developer_company.png)
