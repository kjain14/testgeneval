import time
import os

if __name__ == "__main__":
    while True:
        time.sleep(600)
        os.system("echo y | docker system prune -a")
