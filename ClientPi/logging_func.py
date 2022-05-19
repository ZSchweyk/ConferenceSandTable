

def LOG(string: str):
    with open("/home/pi/projects/log.txt", "a") as file:
        file.write(string)
        file.write("")


def CLEAR_LOG():
    with open("/home/pi/projects/log.txt", "w") as file:
        file.write("")


