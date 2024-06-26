import os
import sys
from configparser import ConfigParser
from massa_k.weight_manager import WeightManager

ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)
CONFIG_PATH = os.path.join(ROOT_PATH, "bin", "config.ini")

VERSION = '0.2.1'


def exception_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("\n\n *** Программа завершена пользователем ***\n\n")
    else:
        sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":

    sys.excepthook = exception_hook

    # Load config
    if not os.path.exists(CONFIG_PATH):
        print("Ошибка. Отсутствует конфигурационный файл", CONFIG_PATH)
        input("Нажмите Enter чтобы закрыть окно")

    print("")
    print("***********************************************************")
    print("******* Сбор и архивирование данных с весов Масса-К *******")
    print("***********************************************************")
    print("v", VERSION, sep="")
    print("")
    print("Загрузка настроек", CONFIG_PATH, "...")

    config = ConfigParser()
    config.read(CONFIG_PATH)
    host = config.get("Network", "ip")  # IP address
    port = int(config.get("Network", "port"))  # The port
    data_folder_path = (config.get("Path", "data_folder_path"))  # The port

    min_mass = float(config.get("Weighing", "min_mass"))

    print("Папка с данными взвешивания:", data_folder_path)

    # Управление взвешиванием
    weight_manager = WeightManager(host, port, data_folder_path, min_mass)
    weight_manager.start()

    # input("Нажмите Enter чтобы закрыть окно")
