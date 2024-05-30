import os
import time
from datetime import datetime
from threading import Thread

from openpyxl.reader.excel import load_workbook

from massa_k.massa_k_scales import MassaKScales
from openpyxl import Workbook


class WeightManager(Thread):

    SEND_INTERVAL = 0.1  # seconds
    DATA_FOLDER_PATH = './data/'

    def __init__(self, host, port):
        super().__init__()
        self.__is_started = False
        self.__cur_file_path = ''
        self.__workbook = None
        self.__sheet = None
        self.__next_id = 0

        print("Подключение к ", host, "...")
        self._scales = MassaKScales(host, port)
        if self._scales.is_connected:
            print("Подключено!")
            self._scales.add_weight_event_handler(self.weight_event_handler)
            self._scales.start()
            self.start()
        else:
            print("Ошибка соединения с весами! IP: ", host, " , port: ", port)

        self.check_change_day()

    def check_change_day(self):
        # Create data folder if not exist
        if not os.path.exists(self.DATA_FOLDER_PATH):
            os.makedirs(self.DATA_FOLDER_PATH)

        cur_date_time_str = datetime.now().strftime('%d-%m-%Y')
        # cur_date_time_str = datetime.now().strftime('%d-%m-%Y_%H-%M')
        new_file_path = self.DATA_FOLDER_PATH + cur_date_time_str + '.xlsx'

        if self.__cur_file_path != new_file_path:
            if self.__workbook is not None:
                self.__workbook.save(self.__cur_file_path)

            self.__cur_file_path = new_file_path

            if os.path.exists(self.__cur_file_path):
                self.__workbook = load_workbook(self.__cur_file_path)
                self.__sheet = self.__workbook.active
                self.__next_id = self.__sheet.max_row + 1
            else:
                self.__workbook = Workbook()
                self.__sheet = self.__workbook.active
                self.__next_id = 1

    def weight_event_handler(self, mass):
        self.check_change_day()
        current_time_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.__sheet.append([self.__next_id, current_time_str, float(mass)])
        self.__next_id += 1
        self.__workbook.save(self.__cur_file_path)

        print(current_time_str, " Масса:", mass, "г.")

    def run(self) -> None:
        self.__is_started = True
        while self.__is_started:
            self._scales.send_command()
            time.sleep(self.SEND_INTERVAL)

    def stop(self):
        self.__is_started = False
