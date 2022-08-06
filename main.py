from requests_html import AsyncHTMLSession, HTMLSession
from string import ascii_letters, digits
from secrets import choice
from time import time
from colorama import init, Fore
import csv
import os.path
import asyncio
from datetime import datetime

num = 10  # size of string
DEBUG: bool = True
urls = []
scrap_url = "https://anonfiles.com/"
amount = 200  # (works fine with 200)
text_title = '''
    ___                      _____ __             _______ __             _______           __         
   /   |  ____  ____  ____  / __(_) /__  _____   / ____(_) /__  _____   / ____(_)___  ____/ /__  _____
  / /| | / __ \/ __ \/ __ \/ /_/ / / _ \/ ___/  / /_  / / / _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/
 / ___ |/ / / / /_/ / / / / __/ / /  __(__  )  / __/ / / /  __(__  )  / __/ / / / / / /_/ /  __/ /    
/_/  |_/_/ /_/\____/_/ /_/_/ /_/_/\___/____/  /_/   /_/_/\___/____/  /_/   /_/_/ /_/\__,_/\___/_/                                                                                                                                                                                             
'''


def WriteCSV(row1, row2, row3, row4, row5):
    """write or create csv file"""
    with open('data-list.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([row1, row2, row3, row4, row5])


def resultsCheck(result):
    for i in result:
        if i is not None:
            print(Fore.GREEN + "Saving " + i + " into CSV..")
            sync_driver = HTMLSession()
            sess = sync_driver.get(i)
            with open('data-list.csv', 'r', newline='', encoding='utf-8') as f:
                row_count = sum(1 for _ in f)
                try:
                    title = sess.html.xpath("//h1[@class='text-center text-wordwrap']", first=True).text
                except AttributeError:
                    title = ""
                date = datetime.now()
                WriteCSV(str(row_count), title, sess.url, date.strftime("%H:%M:%S"), date.strftime("%d-%m-%Y"))
            sync_driver.close()


async def work(driver, url):
    session = await driver.get(url)
    print(Fore.GREEN + "testing url: " + Fore.WHITE + url, end="")
    if len(session.html.xpath("//h1[@class='text-center']")) > 0 and len(
            session.html.xpath("//h1[@class='text-center text-wordwrap']")) == 0:
        print(Fore.RED + " doesn't exists")
        return None
    else:
        print(Fore.GREEN + " exists!")
        return session.url


async def main():
    global driver
    urls = []
    for _ in range(1, amount):
        result = ''.join(choice(ascii_letters + digits) for _ in range(num))
        urls.append(f'' + scrap_url + str(result))
    async_driver = AsyncHTMLSession()
    file_url = (work(async_driver, url) for url in urls)
    return await asyncio.gather(*file_url)


if __name__ == "__main__":
    try:
        init(convert=True)
        print(
            text_title + Fore.CYAN
            + "Anonfiles files finder - By Saschax\n"
            + Fore.MAGENTA
            + "\nThe program "
              "automatically searches "
              "for working Anonfiles "
              "files and saves them "
              "in the current path as "
              "a csv file.\n- CTRL + "
              "C to stop program\n")
        if not os.path.isfile('data-list.csv'):
            if DEBUG:
                print(Fore.YELLOW + "creating new csv file..")
            WriteCSV("number", "title", "url", "time", "date")

        amount = int(input(Fore.MAGENTA + "enter the number of async processes to start the program: \n"))
        while True:
            timer_start = time()
            res = asyncio.run(main())
            resultsCheck(res)
            print(Fore.MAGENTA + str(round((time() - timer_start) / amount, 4)) + " seconds per task")
            print(Fore.MAGENTA + str(round((time() - timer_start), 4)) + " seconds for all " + str(amount) + " tasks")

    except KeyboardInterrupt:
        if DEBUG:
            print(Fore.YELLOW + " stopping program")
