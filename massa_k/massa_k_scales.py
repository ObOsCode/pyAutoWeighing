import socket
import time
from threading import Thread


class WeightManager(Thread):

    SEND_INTERVAL = 5200

    def __init__(self, host, port):
        super().__init__()
        self.__is_started = False
        self._scales = MassaKScales(host, port)
        self._scales.start()

    def run(self) -> None:
        self.__is_started = True
        while self.__is_started:
            self._scales.send_command()
            time.sleep(self.SEND_INTERVAL)

    def stop(self):
        self.__is_started = False


class MassaKScales(Thread):

    def __init__(self, host, port):
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__is_started = False

    def send_command(self) -> None:
        print("send command!!!!")
        self.__socket.send(b'\x4A')

    def run(self) -> None:
        self.__is_started = True
        print("START")
        while self.__is_started:

            data = self.__socket.recv(1024)

            print(f"Received {data!r}")

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