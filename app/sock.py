import socket
def get_ip_address():
    """
    :return: get connected ip address of compiling machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

