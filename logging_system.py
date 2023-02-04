import os
from datetime import datetime


class Logging:
    def __init__(self):
        """define variables and standard"""
        self.path_file = None
        self.date_now = None

        self.encoding = 'iso-8859-1'
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.file_starting_name = "anonfiles_scrapper"
        self.folder_name = "logging"

        self.__create_log_folder()

    def info(self, string):
        """writing info message into file"""
        self.__writing("[INF]", string)

    def warning(self, string):
        """writing warning message into file"""
        self.__writing("[WRN]", string)

    def __create_log_folder(self):
        """create log folder if not exists"""
        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)

    def __update_file_name(self):
        """updating file name with current date in "%Y-%m-%d" format"""
        if self.date_now != datetime.today().strftime("%Y-%m-%d"):
            self.date_now = datetime.today().strftime("%Y-%m-%d")
            self.path_file = os.path.join(self.path, self.folder_name,
                                          self.file_starting_name + "_" + self.date_now + ".log")

    def __writing(self, alarm_type, string):
        """writing into log file """
        self.__update_file_name()
        datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f'{self.path_file}', 'a', newline='', encoding=self.encoding) as f:
            f.write(datetime_now + " " + alarm_type + ": " + string + "\n")


logging = Logging()  # assigning logging instance so only activating it once
