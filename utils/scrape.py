import argparse
import requests
import os
import random

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
                help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
                help="path to output directory of images")
args = vars(ap.parse_args())

rows = open(args["urls"]).read().strip().split("\n")
total = 0

random.shuffle(rows)

for url in rows:
    try:
        # try to download the image
        r = requests.get(url, timeout=14)

        # save the image to disk
        p = os.path.sep.join([args["output"], "{}.jpg".format(
            'mA' + str(total).zfill(8))])
        f = open(p, "wb")
        f.write(r.content)
        f.close()

        # update the counter
        print("[INFO] downloaded: {}".format(p))
        total += 1

    # handle if any exceptions are thrown during the download process
    except Exception:
        print("[INFO] error downloading {}...skipping".format(p))
