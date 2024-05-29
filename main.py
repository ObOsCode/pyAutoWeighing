import sys

from massa_k.weight_manager import WeightManager


def exception_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print("\n\n *** Программа завершена пользователем ***\n\n")
    else:
        sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":

    sys.excepthook = exception_hook

    HOST = "192.168.8.1"  # IP address
    PORT = 5001  # The port

    weight_manager = WeightManager(HOST, PORT)
    weight_manager.start()
