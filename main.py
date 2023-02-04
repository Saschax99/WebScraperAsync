import asyncio
import csv
import os.path
import warnings
from secrets import choice
from string import ascii_letters, digits
from time import time

from colorama import init, Fore
from requests_html import AsyncHTMLSession, HTMLSession

from logging_system import logging

warnings.filterwarnings('ignore')

num = 10  # size of string
urls = []
scrap_url = "https://anonfiles.com/"
csv_file_name = "data-list.csv"
amount = 200  # (works fine with 200)
amount_tasks = 0
text_title = '''
    ___                      _____ __             _______ __             _______           __         
   /   |  ____  ____  ____  / __(_) /__  _____   / ____(_) /__  _____   / ____(_)___  ____/ /__  _____
  / /| | / __ \/ __ \/ __ \/ /_/ / / _ \/ ___/  / /_  / / / _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/
 / ___ |/ / / / /_/ / / / / __/ / /  __(__  )  / __/ / / /  __(__  )  / __/ / / / / / /_/ /  __/ /    
/_/  |_/_/ /_/\____/_/ /_/_/ /_/_/\___/____/  /_/   /_/_/\___/____/  /_/   /_/_/ /_/\__,_/\___/_/                                                                                                                                                                                             
'''


def write_into_csv_file(row1, row2, row3):
    """write or create csv file"""
    with open(csv_file_name, 'a', newline='', encoding='iso-8859-1') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([row1, row2, row3])


def check_result(result):
    for i in result:
        if i is not None:
            print(Fore.GREEN + "Saving " + i + " into CSV..")
            syncDriver = HTMLSession()
            sess = syncDriver.get(i)
            with open(csv_file_name, 'r', newline='', encoding='iso-8859-1') as f:
                row_count = sum(1 for row in f)
                try:
                    title = sess.html.xpath("//h1[@class='text-center text-wordwrap']", first=True).text
                except AttributeError:
                    title = ""
                write_into_csv_file(str(row_count), title, sess.url)
                logging.info(f"saving {sess.url} into {csv_file_name}!")
            syncDriver.close()


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


async def main(urls):
    global driver
    urls = []
    for _ in range(1, amount):
        res = ''.join(choice(ascii_letters + digits) for x in range(num))
        urls.append(f'' + scrap_url + str(res))
    AsyncDriver = AsyncHTMLSession()
    fileURL = (work(AsyncDriver, url) for url in urls)
    return await asyncio.gather(*fileURL)


if __name__ == "__main__":
    try:
        init(convert=True)
        print(
            text_title + Fore.CYAN + "Anonfiles files finder - By Saschax\n" + Fore.MAGENTA + "\nThe program "
                                                                                              "automatically searches "
                                                                                              "for working Anonfiles "
                                                                                              "files and saves them "
                                                                                              "in the current path as "
                                                                                              "a csv file.\n- CTRL + "
                                                                                              "C to stop program\n")
        if not os.path.isfile(csv_file_name):
            write_into_csv_file("number", "title", "url")

        amount = int(input(Fore.MAGENTA + "enter the number of async processes to start the program: \n"))

        logging.info("started")
        logging.info(f"amount per period set to {str(amount)}")

        while True:
            timer_start = time()
            res = asyncio.run(main(urls))
            check_result(res)
            print(Fore.MAGENTA + str(round((time() - timer_start) / amount, 4)) + " seconds per task")
            print(Fore.MAGENTA + str(round((time() - timer_start), 4)) + " seconds for all " + str(amount) + "tasks")
            amount_tasks = amount_tasks + 1

            logging.info(
                f"ended cycle number {amount_tasks} with {amount} tasks within {str(round((time() - timer_start), 4))} seconds")

    except KeyboardInterrupt:
        logging.warning("stopped")
        exit()
