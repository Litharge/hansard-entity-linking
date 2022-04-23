import csv
import requests
import requests.exceptions
from time import sleep


# stores the csv list of mps in a file allowing the user to visualise which mps are known to the system
def save_csv(to_download, save_directory):

    while True:
        try:
            r = requests.get("https://www.theyworkforyou.com/mps/?f=csv&date=" + to_download)
            r.raise_for_status()
            break
        except requests.exceptions.HTTPError as e:
            print(f"server error: {e}")
            sleep(1)
        except requests.exceptions.Timeout as e:
            print(f"timeout: {e}")
            sleep(1)


    decoded = r.content.decode("utf-8")

    with open(save_directory, "w") as f:
        f.write(decoded)





