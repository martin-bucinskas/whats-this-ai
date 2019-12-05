# https://tinyurl.com/uql3eox
from time import sleep

import requests

# response = requests.get('')

URL = 'https://script.googleusercontent.com/macros/echo?user_content_key=NiK51BMsSacnfn-KZR8I5FyLNPRhBlZ' \
      '-CGPKDDZR_6qmnJKvWud7BX8Drj_EUnaDQT_BAvkXYEnsqNMK1uTb24CFTR4Dh7AMm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_' \
      '1xSncGQajx_ryfhECjZEnCQrgJrBr_wq9mqrjLXVxZ6OOccQWSnI5SA_c0mvm9zKuXgRWEwLqj2TOQiGIQt7_hdIug5zkO6q&' \
      'lib=MuVsdrfoaGZEmjU4z1ag2pPoH_GRKR_iH '

with open("training-set.txt", "r+") as f:
    while True:
        print('...')
        response = requests.get(URL)
        text_response = response.text

        print(response)
        print(text_response)

        if text_response not in f.read():
            text_response = text_response + '\n'
            f.write(text_response)
        else:
            print('Already in set.')
        sleep(1)
