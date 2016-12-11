import os
import time
import requests

while True:
    workers = list()
    files = os.listdir('check_files')
    #print(files)
    for file in files:
        f = open('check_files/'+file)
        for line in f:
            workers.append(line)
        f.close()
        os.remove('check_files/'+file)
    e = 0
    while e < len(workers):
        print('checking')
        cur_time = time.time()
        worker = workers[e].split(' ')
        if float(worker[1][:-1]) < cur_time:
            print('sending request')
            req = ('https://api.telegram.org/bot245955280:AAHZ'
                   'LjKyAvPXDA4z92d9h02jjH_CQiuO4b0/sendmessage'
                   '?chat_id='
                   )
            req += str(worker[0])
            req += '&text=Продавец вернулся c точки\n'
            requests.post(req)
            e += 1
        else:
            time.sleep(60)