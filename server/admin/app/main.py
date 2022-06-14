from db_remover import remove
from time import sleep
import traceback


# one week
time = 60 * 60 * 24 * 7


if __name__ == '__main__':
    while True:
        try:
            remove()
        except:
            traceback.print_exc()
        sleep(time)
