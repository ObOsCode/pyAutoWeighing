import socket
from threading import Thread
from typing import Callable

from pyrobotics.event import Event


class MassaKScales(Thread):

    SCALES_INFO_COMMAND = b'\x4A'

    def __init__(self):
        super().__init__()
        self.__socket = None
        self.__weightingEvent = Event()
        self.is_connected = False
        self.__is_started = False

    def connect(self, host, port):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((host, port))
        except TimeoutError:
            print("Socket connection TimeoutError!")
        except ConnectionError:
            print("Socket connection error!")
        except OSError as err:
            print("Socket connection OSError!", err)
        except SystemError:
            print("System error!")
        except Exception as err:
            print(f"Socket connection Unexpected error {err=}, {type(err)=}")

        else:
            self.is_connected = True

    def send_command(self) -> None:
        try:
            self.__socket.send(self.SCALES_INFO_COMMAND)
        except ConnectionError:
            print("Socket send error!")
            self.is_connected = False
            self.__socket.close()
        except OSError as err:
            print("Socket connection OSError!", err)
        except Exception as err:
            print(f"Socket connection Unexpected error {err=}, {type(err)=}")

    def add_weight_event_handler(self, handler: Callable):
        self.__weightingEvent.handle(handler)

    def run(self) -> None:
        self.__is_started = True
        is_weight_now = False

        while self.__is_started:

            if not self.is_connected:
                continue

            try:
                data = self.__socket.recv(1024)
            except ConnectionError:
                print("Socket receive error!")
                self.is_connected = False
                self.__socket.close()
                continue
            except TimeoutError:
                print("Socket receive timeout error!")
                self.is_connected = False
                self.__socket.close()
                continue

            except OSError as err:
                print("OSError!", err)
                self.is_connected = False
                self.__socket.close()
                continue

            except SystemError:
                print("System error!")
                self.is_connected = False
                self.__socket.close()
                continue

            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                self.is_connected = False
                self.__socket.close()
                continue

            is_minus = (data[4] >> 7) & 1
            is_finished = (data[0] >> 7) & 1
            is_zero = (data[0] >> 6) & 1
            # is_net = (data[0] >> 5) & 1

            mass = 0
            mass |= (data[4] & 0b1111111) << 16
            mass |= data[3] << 8
            mass |= data[2]

            discreteness = data[1]  # 0 - в граммах, 1 - в десятых грамма

            if discreteness == 1:
                mass /= 10
            # elif discreteness == 4:
            #     mass *= 10
            # elif (discreteness == 5) or (discreteness == 6):
            #     mass *= 100
            if is_minus:
                mass = -mass

            if is_weight_now and is_finished and (not is_zero):
                is_weight_now = False
                self.__weightingEvent.fire(mass)  # dispatch event

            if not is_finished:
                is_weight_now = True


'''
unsigned short CRC16(unsigned short crc, unsigned char *buf, unsigned short len)
{ 
    unsigned short bits, k ,a, temp;
    crc=0;
    for (k=0; k<len; k++)
    {
        a=0; temp=(crc>>8)<<8;
        for (bits=0;bits<8;bits++)
        {
            if ((temp ^ a) & 0x8000) a=(a<<1) ^ 0x1021; else a<<=1;
            temp<<=1;
        }
    crc=a ^ (crc<<8) ^ (buf[k] & 0xFF);
    }
    return(crc);
}
'''