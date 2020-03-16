from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('igotoworld')
    process.crawl('allo')
    process.start()


def task1():
    print("Task 1:")
    root = etree.parse("task1.xml")
    avg = root.xpath("count(//fragment[@type='image']) div count(//page)")
    print("Average amount of images on page: %.2f" % avg)


def task2():
    print("Task 2:")
    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    print("XHTML page will be opened in browser")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    print("Cleanup", end='', flush=True)
    cleanup()
    print("Scrapping data", end='', flush=True)
    scrap_data()
    print("finished")
    while True:
        print("-------------------------------------------")
        print("1. Task1 (IGoToWorld)\n"
              "2. Task2 (Allo)")
        print("> ", end='', flush=True)
        number = input()
        if number == "1":
            task1()
        elif number == "2":
            task2()
        else:
            break
