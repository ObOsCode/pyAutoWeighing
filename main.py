
from massa_k.massa_k_scales import WeightManager


if __name__ == "__main__":

    HOST = "192.168.8.1"  # IP address
    PORT = 5001  # The port

    weight_manager = WeightManager(HOST, PORT)
    weight_manager.start()




