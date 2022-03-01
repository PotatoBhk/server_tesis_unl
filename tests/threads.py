import logging
from threading import Thread

import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(3)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    x = Thread()
    # logging.info("Main    : before creating thread")
    # x = threading.Thread(target=thread_function, args=("ej",))
    # logging.info("Main    : before running thread")
    # logging.info("Thread is alive: {}".format(x.is_alive()))    
    # x.start()
    # logging.info("Thread is alive: {}".format(x.is_alive()))
    # logging.info("Main    : wait for the thread to finish")
    # # x.join()
    # logging.info("Main    : all done")
    
    for i in range(3):
        logging.info("Attemp: {}".format(i))
        if not x.is_alive():
            x = Thread(target=thread_function, args=("ej",))
            x.start()
    