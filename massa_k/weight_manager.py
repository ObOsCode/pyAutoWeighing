import time
from datetime import datetime
from threading import Thread
from massa_k.massa_k_scales import MassaKScales
from openpyxl import Workbook


class WeightManager(Thread):

    SEND_INTERVAL = 0.1  # seconds
    DATA_FILE_PATH = 'data/data.xlsx'

    def __init__(self, host, port):
        super().__init__()
        self.__is_started = False

        self.__workbook = Workbook()
        self.__sheet = self.__workbook.active
        self.__sheet.append(["ID", "Время", "Масса"])
        self.__next_id = 1  # Инициализируем ID записи

        self._scales = MassaKScales(host, port)
        self._scales.add_weight_event_handler(self.weight_event_handler)
        self._scales.start()

    def weight_event_handler(self, mass):
        print("==============================================")
        print("Mass: ", mass)

        current_time = datetime.now().strftime('%H:%M:%S')
        self.__sheet.append([self.__next_id, current_time, float(mass)])
        self.__next_id += 1
        self.__workbook.save(self.DATA_FILE_PATH)

    def run(self) -> None:
        self.__is_started = True
        while self.__is_started:
            self._scales.send_command()
            time.sleep(self.SEND_INTERVAL)

    def stop(self):
        self.__is_started = False
