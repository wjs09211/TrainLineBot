import os
import requests
import json
from datetime import datetime
import hashlib
import threading
import time
import logging
from api.trainCrawler.entities.trainTicket import TrainTicket
from api.exceptions import QueryExistSeatException
logging.basicConfig(level=logging.INFO)
HOST = 'https://www.railway.gov.tw'
SECRET_KEY = 'eeit8910venom'

class TrainCrawler:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Linux; Android 5.1.1; R7sf Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.73 Mobile Safari/537.36/Worklight/8.0.0.00.2015-12-11T23:31:24Z'
        self.session = requests.Session()
        self.header = {'User-Agent': self.user_agent,
                       "Content-Type": "application/json;charset=UTF-8",
                       'lang': 'zh-TW',
                       'code': '',
                       'deviceId': '2c4d54e908045751'
                       }

    def _setting_secret_key(self):
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        self.header['time'] = current_time
        sha = hashlib.sha256()
        sha.update((SECRET_KEY + current_time).encode("utf-8"))
        code = sha.hexdigest()
        self.header['code'] = code

    def query_exist_seat(self, customerId='A121360824', trnClassCodes=None, startStaCode='1000',
                         endStaCode='3360', startDateTime=datetime.now(), endDateTime=datetime.strptime("2022/03/25-12:00", "%Y/%m/%d-%H:%M")):
        if trnClassCodes == None:
            trnClassCodes = [1, 2, 3, 4, 5]  # 123 普悠瑪 太魯閣 自強 # 45莒光復興
        post_data = {'packages': 'oneWay', 'queryType': 'trnClass', 'tktNorOrderCnt': '1',
                     'isChgSeat': False, 'custIdType': 'PERSON_ID', 'queryByStartTime': True,
                     'favSeat': 'None',
                     'customerId': customerId,
                     'trnClassCodes': trnClassCodes,
                     'startStaCode': startStaCode, 'endStaCode': endStaCode,
                     'startDateTime': startDateTime.strftime("%Y-%m-%d %H:%M:%S")}
        url = HOST + '/tra-tip-web/ptr/pts131/qryseat/time'
        self._setting_secret_key()
        r = self.session.post(url, json=[post_data], headers=self.header)

        remain_seat = json.loads(r.text)
        if remain_seat['message'] == 'OK':
            # logging.info("query seat success")
            for data in remain_seat['data']:
                end_time = endDateTime
                start_time = datetime.strptime(data['startTime'], "%Y-%m-%d %H:%M:%S")
                if start_time <= end_time:
                    ticket = TrainTicket(data['trainNo'], data['startTime'], data['arriveTime'], data['adultTktPrice'], data['trnClassCode'], data['trainLine'])
                    ticket.show_info()
                    return ticket
            return None
        else:
            logging.error("query seat error222")
            logging.error(str(post_data))
            logging.error(str(remain_seat))
            raise QueryExistSeatException

class TrainCrawlerTask(threading.Thread):
    def __init__(self, line_id, parm):
        super().__init__()
        self.line_id = line_id
        self.query_parm = parm
        self.start_date = datetime.now()

    def run(self):
        for i in range(20):
            time.sleep(1)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"%s" % (self.getName(),))
# print(len('a85ae71b84d2c04a7b99a9c46638364c561b26a6f4b934aef95ddd58ec9042d8'))

if __name__ == '__main__':
    train_crawler = TrainCrawler()
    print(train_crawler.query_exist_seat())