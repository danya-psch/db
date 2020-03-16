Лабораторна робота No 1. Вивчення базових операцій обробки XML-документів
=====================

Завдання
-----------------------------------
[Постановка завдання](http://scs.kpi.ua/sites/default/files/lab1_bd2-db2019_2020.docx.pdf)

Варіант завдання
-----------------------------------
15 варінт згідно номема у списку

| Базова сторінка (завдання 1) | Зміст завдання 2 | Адреса інтернет-магазину (завдання 3)| 
|-------------|-----------|-----------|
| [ua.igotoworld.com](https://ua.igotoworld.com) | Середня кількість графічних фрагментів | [allo.ua](https://allo.ua) |

Лістинг коду
-----------------------------------
Збирання даних зі сторінки [ua.igotoworld.com](https://ua.igotoworld.com)
```
src/lab1/spiders/igotoworld.py
```

```python
class IgotoworldSpider(scrapy.Spider):
    name = 'igotoworld'
    allowed_domains = ['ua.igotoworld.com']
    start_urls = ['https://ua.igotoworld.com/ua/news_list/news.htm']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'http')]")
        all_text = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()"
        )
        yield {
            'url': response.url,
            'payload': [
                           {
                               'type': 'text',
                               'data': text.get().strip()
                           } for text in all_text
                       ] +
                       [
                           {
                               'type': 'image',
                               'data': image.get()
                           } for image in all_images
                       ]
        }
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., 'https://ua.igotoworld.com/')][substring(., string-length() - 3) = '.htm']"
            )
            selected_links = [link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)

```

Збирання даних зі сторінки [allo.ua](https://allo.ua)
```
src/lab1/spiders/allo.py
```

```python
class AlloSpider(scrapy.Spider):
    name = 'allo'
    allowed_domains = ['allo.ua']
    start_urls = ['https://allo.ua/ua/velosipedy/']

    def start_requests(self):  #was a mistake without it (INFO: Ignoring response <403 https://allo.ua/ua/velosipedy/>: HTTP status code is not handled or not allowed)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response: Response):
        products = response.xpath("//ul[(contains(@class, 'products-grid'))]/li[contains(@class, 'item')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//a[contains(@class, 'product-name')]/span/text()[1]").get(),
                'price': product.xpath(".//span[contains(@class, 'new_sum')]/text()[1]").get(),
                'img': product.xpath(".//img/@src").get()
            }
```

Запис зібраних даних до файлів
```
src/lab1/pipelines.py
```

```python
class Lab1Pipeline(object):
    def open_spider(self, spider):
        self.root = etree.Element("data" if spider.name == "igotoworld" else "shop")

    def close_spider(self, spider):
        with open('task%d.xml' % (1 if spider.name == "igotoworld" else 2), 'wb') as f:
            f.write(etree.tostring(self.root, encoding="UTF-8", pretty_print=True, xml_declaration=True))

    def process_item(self, item, spider):
        if spider.name == "igotoworld":
            page = etree.Element("page", url=item["url"])
            for payload in item["payload"]:
                fragment = etree.Element("fragment", type=payload["type"])
                fragment.text = payload["data"]
                page.append(fragment)
            self.root.append(page)
        else:
            product = etree.Element("product")
            desc = etree.Element("description")
            desc.text = item["description"]
            pr = etree.Element("price")
            pr.text = item["price"]
            img = etree.Element("image")
            img.text = item["img"]
            product.append(desc)
            product.append(pr)
            product.append(img)
            self.root.append(product)
        return item
```

Завдання №1
```
src/main.py
```

```python
def task1():
    print("Task 1:")
    root = etree.parse("task1.xml")
    avg = root.xpath("count(//fragment[@type='image']) div count(//page)")
    print("Average amount of images on page: %.2f" % avg)
```

Завдання №2
```
src/main.py
```

```python
def task2():
    print("Task 2:")
    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    print("XHTML page will be opened in browser")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))

```

```
src/task2.xsl
```

```xsl
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output
        method="xml"
        doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
        doctype-public="-//W3C//DTD XHTML 1.1//EN"
        indent="yes"
    />
    <xsl:template match="/">
        <html xml:lang="en">
            <head>
                <title>Task 2</title>
            </head>
            <body>
                <h1>Products:</h1>
                <xsl:apply-templates select="/shop"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="/shop">
        <table border="1">
            <thead>
                <tr>
                    <td>Image</td>
                    <td>Description</td>
                    <td>Price(UAH)</td>
                </tr>
            </thead>
            <tbody>
                <xsl:apply-templates select="/shop/product"/>
            </tbody>
        </table>
    </xsl:template>
    <xsl:template match="/shop/product">
        <tr>
            <td>
                 <xsl:apply-templates select="image"/>
            </td>
            <td>
                <xsl:apply-templates select="description"/>
            </td>
            <td>
                <xsl:apply-templates select="price"/>
            </td>
        </tr>
    </xsl:template>
    <xsl:template match="image">
        <img alt="image of product">
            <xsl:attribute name="src">
                <xsl:value-of select="text()"/>
            </xsl:attribute>
        </img>
    </xsl:template>
    <xsl:template match="price">
        <xsl:value-of select="text()"/>
    </xsl:template>
    <xsl:template match="description">
        <xsl:value-of select="text()"/>
    </xsl:template>
</xsl:stylesheet>
```

Лістинг згенерованих файлів
-----------------------------------
```
task1.xml
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<data>
  <page url="https://ua.igotoworld.com/ua/news_list/news.htm">
    <fragment type="text">Новини України  - Останні новини про туризм, подорожі та відпочинок</fragment>
    <fragment type="text">Косівську кераміку внесли до переліку нематеріальної спадщини ЮНЕСКО</fragment>
    <fragment type="text">Музей народного мистецтва та побуту Гуцульщини, Косів</fragment>
    <fragment type="text">вул. Незалежності 55, м. Косів 78600, Івано-Франківська обл., Україна</fragment>
    <fragment type="text">Приємна новина для поціновувачів народної творчості – Косівську мальовану кераміку внесли до переліку нематеріальної культурної спадщини ЮНЕСКО.</fragment>
    <fragment type="text">У Дніпрі відбувся наймасштабніший науково-популярний фестиваль Східної Європи</fragment>
    <fragment type="text">вул. Космічна 20, м Дніпропетровськ, Дніпропетровська обл., Україна</fragment>
    <fragment type="text">У Дніпрі відбувся наймасштабніший науково-популярний фестиваль Східної Європи – Interpipe TechFest 2019. Започаткований у 2016 році, цей захід щороку приваблює усе більше учасників та відвідувачів. Цього року до Дніпра з’їхалося понад 120 учасників технічних змагань, 36 спікерів – професіоналів своєї області та лідерів думок, у технічних змаганнях взяли участь більше 220 школярів.</fragment>
    <fragment type="text">У Кривому Розі встановлять найвищий пам'ятник Володимиру Великому</fragment>
    <fragment type="text">У Кривому Розі (Дніпропетровська область) незабаром буде встановлено пам'ятник князю Київської Русі Володимиру Великому. Бронзову восьмиметрову скульптуру вже відлито. Висота постаменту складе 14 метрів. Таким чином, загальна висота пам'ятника буде 22 метри, і він стане найвищим пам'ятником Володимиру Великому в Україні та Європі.</fragment>
    <fragment type="text">У дніпровського комплексу CASCADE PLAZA найкраща ілюмінація</fragment>
    <fragment type="text">Дніпровський комплекс CASCADE PLAZA відзначений нагородами за унікальне освітлення свого фасаду. Спочатку на престижному Нью-Йоркському конкурсі IES Illumination Awards, який відзначає кращі світлові рішення на архітектурних спорудах світу. Потім і на українському конкурсі Ukrainian Urban Awards 2018 у Києві.</fragment>
    <fragment type="text">У Мукачеві з'явився «гусячий» маршрут</fragment>
    <fragment type="text">У центрі Мукачева (Закарпатська область) встановили третю скульптуру гусака і завершили формування першої частини «гусячого» туристичного маршруту. Дві бронзові скульптури гусей, створені скульптором Степаном Федориним, прикрасили місто ще в 2016 році. Це гусак-фотограф і гусак-турист. Тепер же їх доповнив гусак-пивовар.</fragment>
    <fragment type="text">У Києві встановили пам'ятник видатному співакові</fragment>
    <fragment type="text">У столиці, на перехресті проспекту Чорновола та вулиці Січових Стрільців, відкрили сквер імені Мусліма Магомаєва і встановили там пам'ятник широко відомому оперному і естрадному співакові. Сталося це з ініціативи та за підтримки посольства Азербайджану в межах святкування 75-річчя від дня народження Магомаєва.</fragment>
    <fragment type="text">Для віз до Канади тепер потрібна біометрія</fragment>
    <fragment type="text">Для отримання віз до Канади українцям потрібно здавати біометричні дані: відбитки пальців і біометричні фото. Біометрія буде вимагатися для отримання туристичних віз, дозволів на навчання і роботу (за винятком громадян США), для постійного проживання, для отримання статусу біженця.</fragment>
    <fragment type="text">З'явилася віртуальна прогулянка Запоріжжям</fragment>
    <fragment type="text">Ви ще не були в Запоріжжі? Поки не виходить поїхати? Тоді до «живого» знайомства з цікавим містом можна познайомитися з ним віртуально. Запоріжжям проводиться віртуальний тур.</fragment>
    <fragment type="text">Устрична ферма на Тилігульському лимані чекає туристів</fragment>
    <fragment type="text">Устрична ферма «Устриці Скіфії» на березі Тилігульського лиману (Миколаївська область), недалеко від курорту Коблево, відкрита для туристів. Тут на свіжому повітрі можна насолодитися ніжним м'ясом устриць з тонким морським ароматом і вином. Унікальні устриці вирощують в екологічно чистій акваторії Чорного моря, в природному національному парку.</fragment>
    <fragment type="text">9 мільйонів чоловік побачили аеропорти України в першому півріччі</fragment>
    <fragment type="text">Пасажиропотік через аеропорти України в першому півріччі склав 8,9 мільйона чоловік. Це на 26,0% більше, ніж за аналогічний період минулого року, і взагалі рекордний показник для України.</fragment>
    <fragment type="text">© IGotoWorld.com - Your GUIDE TO the WORLD. Всі права захищені.</fragment>
    <fragment type="text">Копіювання матеріалів без дозволу адміністрації сайту заборонено.</fragment>
    <fragment type="text">Ми цінуємо Вашу увагу і час, проведений з нами на сайті IGotoWorld.com. Якщо у Вас є запитання, побажання, скарги або ж Ви бажаєте більше дізнатись про нас, оберіть пункт, що Вас цікавить, і пройдіть за посиланням. Ми обов’язково приділимо Вам увагу.</fragment>
    <fragment type="text">Проблеми з використанням ресурсу</fragment>
    <fragment type="image">https://www.facebook.com/tr?id=1676725735920309&amp;ev=PageView&amp;noscript=1</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ua.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ua.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ru.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-en.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/homeIcon.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/TOP/top-sil-ua.gif</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2707191_170x128_2701914_800x600_0-02-04-8409352abbbd747fbbda961112348330537314c370edd265a83e3ed2df4747d7_33fb6a25.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2705737_170x128_IMG_9064.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684832_170x128_Vladimir.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684801_170x128_Kompleks-1.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684630_170x128_Gus.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684680_170x128_Magomaev.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684642_170x128_Biometrija.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684629_170x128_HorticjaTetianaSmirnovaIGotoWorldPhotoGroup.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684664_170x128_Ustricy.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2684628_170x128_BorispolTetianaSmirnovaIGotoWorldPG.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/logo-small.png</fragment>
  </page>
  <page url="https://ua.igotoworld.com/ua/news_list/1042-news-ivano-frankivsk.htm">
    <fragment type="text">Новини Івано-Франківська  - Останні новини про туризм, подорожі та відпочинок</fragment>
    <fragment type="text">Новини Івано-Франківська область</fragment>
    <fragment type="text">У Франківську пройде фестиваль народного одягу</fragment>
    <fragment type="text">пров. Фортечний 1, м. Івано-Франківськ 76000, Україна</fragment>
    <fragment type="text">Свої колекції представлять сучасні дизайнери. Фестиваль покликаний популяризувати народний одяг Карпатського регіону. Відбудеться перший фест уже невдовзі — 5 травня.</fragment>
    <fragment type="text">В Івано-Франківську встановили нові скульптури</fragment>
    <fragment type="text">пл. Ринок, Івано-Франківськ 76000, Україна</fragment>
    <fragment type="text">Івано-Франківськ відтепер має нові туристичні родзинки. Колекцію кованих скульптур, що розміщені у центральній частині міста, поповнили ще дві. Їх виготовили ковалі на фестивалі ковальського мистецтва у 2016 році.</fragment>
    <fragment type="text">В Івано-Франківську з'явилася підсвітка Фортечного провулку</fragment>
    <fragment type="text">Станіславівська фортеця, Івано-Франківськ</fragment>
    <fragment type="text">пров. Фортечний, Івано-Франківськ 76000, Україна</fragment>
    <fragment type="text">В Івано-Франківську з'явилася гарна кольорова підсвітка Фортечного провулку, де розташована старовинна кріпосна стіна, що залишилася від Станіславівської фортеці. У серпні цього року провулок оновили: почистили стіну від трави, відреставрували фасади, встановили ліхтарі.</fragment>
    <fragment type="text">В Івано-Франківську на екскурсію можна потрапити безкоштовно</fragment>
    <fragment type="text">Таку цікаву акцію у місті організовують вже п’ятий рік поспіль. Стартують такі екскурсії у травні і тривають до кінця серпня.</fragment>
    <fragment type="text">Івано-Франківськ – у Топ-5 найкращих міст Європи</fragment>
    <fragment type="text">Це вже не перший подібний здобуток столиці Прикарпаття. Але попереду ще головний етап – боротьба з чотирма містами Європейського Союзу за першість.</fragment>
    <fragment type="text">PORTO FRANKO ГогольFEST 2016: Івано-Франківськ стане мистецьким центром України</fragment>
    <fragment type="text">вул. Галицька 4а, Івано-Франківськ 76000, Україна</fragment>
    <fragment type="text">8–12 червня 2016 року в Івано-Франківську вперше відбудеться   міжнародний фестиваль «PORTO FRANKO ГогольFEST».</fragment>
    <fragment type="text">© IGotoWorld.com - Your GUIDE TO the WORLD. Всі права захищені.</fragment>
    <fragment type="text">Копіювання матеріалів без дозволу адміністрації сайту заборонено.</fragment>
    <fragment type="text">Ми цінуємо Вашу увагу і час, проведений з нами на сайті IGotoWorld.com. Якщо у Вас є запитання, побажання, скарги або ж Ви бажаєте більше дізнатись про нас, оберіть пункт, що Вас цікавить, і пройдіть за посиланням. Ми обов’язково приділимо Вам увагу.</fragment>
    <fragment type="text">Проблеми з використанням ресурсу</fragment>
    <fragment type="image">https://www.facebook.com/tr?id=1676725735920309&amp;ev=PageView&amp;noscript=1</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ua.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ua.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-ru.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/langs/flag-en.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/homeIcon.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/TOP/top-sil-ua.gif</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2680864_170x128_ukrainskyi-narodnyi-odyag-2.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2211796_170x128_17883674_363670530700590_2147955968644529432_n—kopija.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/2193576_170x128_Fortechniiprovulok,foto.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/1934929_170x128_1.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/1927193_170x128_bezymyannyy.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/file/logo.png</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/websites/1/images/news/1029249_170x128_inside.jpg</fragment>
    <fragment type="image">https://ua.igotoworld.com/frontend/webcontent/images/logo-small.png</fragment>
  </page>
...
</data>
```

```
task2.xml
```

```xml
<?xml version='1.0' encoding='UTF-8'?>
<shop>
  <product>
    <description>Велосипед 24" Formula ACID 2.0 AM 14G DD 12,5" біло-малиновий з блакитним (м) 2019</description>
    <price>3 880</price>
    <image>https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/2/4/24_formula_acid_2.0_dd_-_2019.jpg</image>
  </product>
  <product>
    <description>Велосипед Titan Spider 24" 12" green-black (24TJS18-16-5) 2019</description>
    <price>3 499</price>
    <image>https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/s/p/spider-24_24tjs18-16-5_right_side.jpg</image>
  </product>
  <product>
    <description>Велосипед Rover Centurion Max 29"18" 2019 Black /Grey Green</description>
    <price>4 600</price>
    <image>https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/4/3/430035_1.jpg</image>
  </product>
  <product>
    <description>Велосипед Rover Samson Plus 27.5"18" 2019 Grey/ Yellow Blue</description>
    <price>3 900</price>
    <image>https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/s/a/samson_plus_blakc_yellow_front_.jpg</image>
  </product>
...
</shop>
```

```
task2.xhtml
```

```xhtml
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
  <head>
    <title>Task 2</title>
  </head>
  <body>
    <h1>Products:</h1>
    <table border="1">
      <thead>
        <tr>
          <td>Image</td>
          <td>Description</td>
          <td>Price(UAH)</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <img alt="image of product" src="https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/2/4/24_formula_acid_2.0_dd_-_2019.jpg"/>
          </td>
          <td>Велосипед 24" Formula ACID 2.0 AM 14G DD 12,5" біло-малиновий з блакитним (м) 2019</td>
          <td>3 880</td>
        </tr>
        <tr>
          <td>
            <img alt="image of product" src="https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/s/p/spider-24_24tjs18-16-5_right_side.jpg"/>
          </td>
          <td>Велосипед Titan Spider 24" 12" green-black (24TJS18-16-5) 2019</td>
          <td>3 499</td>
        </tr>
        <tr>
          <td>
            <img alt="image of product" src="https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/4/3/430035_1.jpg"/>
          </td>
          <td>Велосипед Rover Centurion Max 29"18" 2019 Black /Grey Green</td>
          <td>4 600</td>
        </tr>
        <tr>
          <td>
            <img alt="image of product" src="https://i.allo.ua/media/catalog/product/cache/3/small_image/212x184/9df78eab33525d08d6e5fb8d27136e95/s/a/samson_plus_blakc_yellow_front_.jpg"/>
          </td>
          <td>Велосипед Rover Samson Plus 27.5"18" 2019 Grey/ Yellow Blue</td>
          <td>3 900</td>
        </tr>
	...
      </tbody>
    </table>
  </body>
</html>

```

Приклади роботи програми
-----------------------------------
![](https://github.com/danya-psch/db/blob/master/sem6/lab1/img/task1.png)
![](https://github.com/danya-psch/db/blob/master/sem6/lab1/img/task2.png)
![](https://github.com/danya-psch/db/blob/master/sem6/lab1/img/table.png)

