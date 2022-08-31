import requests
import json
from datetime import datetime
import hashlib
import threading
import time
import logging
from api.trainCrawler.entities.trainTicket import TrainTicket
from api.utils.exceptions import QueryExistSeatException, NoMoneyException
from TrainLineBot import settings


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
        self.booing_ticket_defualt_data = {
            "isHaveSeat": 'true',
            "scheduleNo": 1,
            "startTime": "2022-03-25 12:39:00",
            "arriveTime": "2022-03-25 14:29:00",
            "travelTime": "01:50",
            "transferTime": 0,
            "trainNo": "123",
            "trnClassCode": 3,
            "startStationCode": "1100",
            "endStationCode": "3360",
            "adultTktPrice": 326,
            "halfTktPrice": 163,
            "totalTktCnt": 1,
            "hasStand": 'false',
            "stand": 'false',
            "customerId": "A148451324",
            "custIdType": "PERSON_ID",
            "tktNorOrderCnt": 1,
            "parentChildCnt": 0,
            "wheelChairCnt": 0,
            "isMatchChgSeat": 'false',
            "favSeat": "NONE",
            "isMatchPiority": 'false',
            "queryType": "trnClass",
            "seatKind": 301,
            "ptrTransferList": [
                {
                    "startStaCode": "1100",
                    "endStaCode": "3360",
                    "trnClassCode": 3,
                    "trainNo": "123",
                    "startDateTime": "2022-03-25 12:39:00",
                    "endDateTime": "2022-03-25 14:29:00",
                    "trainOrder": 0,
                    "isOfferBento": 'false',
                    "trnLine": 1,
                    "trainEqCode": {
                        "isWheelChair": "Y",
                        "isBreastFeed": "Y",
                        "isBike": "N",
                        "isParentChildSeat": "Y",
                        "isTableSeat": "N",
                        "isBusinessSeat": "N",
                        "isFreeSeat": "N",
                        "isStandingSeat": "Y",
                        "isReserved": "Y",
                        "isFoodSrv": "Y",
                        "isEveryday": "Y",
                        "isRealName": "N",
                        "isParlorCar": "N",
                        "supplyDinningSections": [],
                        "isEarlyBirdTrn": "N"
                    },
                    "trnDirection": "COUNTERCLOCKWISE",
                    "trnThrough": 1,
                    "trnTypeCode": 1
                }
            ],
            "earlyBirdTkt": 'false',
            "earlyBirdTktDis": 0,
            "trainType": "NORMAL",
            "trainLine": 1,
            "fast": 'false',
            "cheap": 'false'
        }

    def _setting_secret_key(self):
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        self.header['time'] = current_time
        sha = hashlib.sha256()
        sha.update((SECRET_KEY + current_time).encode("utf-8"))
        code = sha.hexdigest()
        self.header['code'] = code

    def query_exist_seat(self, customerId='A148451324', trnClassCodes=None, startStaCode='1000',
                         endStaCode='3360', startDateTime='2022-03-26 12:00:00', endDateTime='2022-03-26 18:00:00'):
        if trnClassCodes == None:
            trnClassCodes = [11, 1, 2, 3, 4, 5]  # 123 普悠瑪 太魯閣 自強 # 45莒光復興
        post_data = {'packages': 'oneWay', 'queryType': 'trnClass', 'tktNorOrderCnt': '1',
                     'isChgSeat': False, 'custIdType': 'PERSON_ID', 'queryByStartTime': True,
                     'favSeat': 'None',
                     'customerId': customerId,
                     'trnClassCodes': trnClassCodes,
                     'startStaCode': startStaCode, 'endStaCode': endStaCode,
                     'startDateTime': startDateTime}
        url = HOST + '/tra-tip-web/ptr/pts131/qryseat/time'
        self._setting_secret_key()
        logging.info('query_exist_seat post')
        r = self.session.post(url, json=[post_data], headers=self.header, timeout=10)
        logging.info('query_exist_seat post finished')

        remain_seat = json.loads(r.text)
        if remain_seat['message'] == 'OK':
            logging.info("query ticket success")
            for data in remain_seat['data']:
                end_time = datetime.strptime(endDateTime, "%Y-%m-%d %H:%M:%S")
                start_time = datetime.strptime(data['startTime'], "%Y-%m-%d %H:%M:%S")
                if start_time <= end_time:
                    logging.info("get ticket")
                    ticket = TrainTicket(data['trainNo'], data['startTime'], data['arriveTime'],
                                         data['adultTktPrice'], data['halfTktPrice'],
                                         data['trnClassCode'], data['trainLine'], startStaCode, endStaCode, customerId)
                    # logging.info(str(ticket))
                    return ticket
            return None
        else:
            logging.error("query seat error222")
            logging.error(str(post_data))
            logging.error(str(remain_seat))
            raise QueryExistSeatException

    def captcha_hack(self):
        # 模擬進入驗證碼頁面，好像是用timestamp去判斷，是誰正在輸入驗證碼頁面吧
        page_url = "https://www.railway.gov.tw/tra-tip-web/ptr/captchaPage?code=797f2700be270c3f500b609a354eab2e&time=" + str(
            int(datetime.timestamp(datetime.now()) * 1000)) + "&lang-code=zh-TW"
        r = self.session.get(page_url)
        # 傳送 google recaptcha 給 2captcha 解碼
        url = "http://2captcha.com/in.php?key=" + settings.CAPTCHA_KEY + "&" \
                                                                "method=userrecaptcha&" \
                                                                "googlekey=6Lc-7S0UAAAAADOtGzfjgtWpzqx5YPBiG-0uZC0O&" \
                                                                "pageurl=" + page_url
        r = requests.get(url)
        logging.info("response for 2captcha.com/in.php " + r.text)
        try:
            status, captcha_process_id = r.text.split('|')
        except:
            logging.error("Send data to 2captcha error, maybe no Money. status code:" + r.text)
            raise NoMoneyException

        # get 2captcha result, retry 8 times
        time.sleep(10)
        for i in range(30):
            time.sleep(1)
            r = requests.get('http://2captcha.com/res.php?key='
                             + settings.CAPTCHA_KEY + '&action=get&id=' + captcha_process_id)
            logging.info("response for 2captcha.com/res.php " + r.text)
            try:
                result = r.text
                if result == "CAPCHA_NOT_READY":
                    continue
                status, captcha_code = r.text.split('|')
                if status == 'OK':
                    r = self.session.get(HOST + "/recaptcha/success?" + captcha_code)
                    return captcha_code
            except:
                logging.error("Get 2captcha result error, maybe no Money. status code:" + r.text)
        return None

    def booking_ticket(self, ticket: TrainTicket, captcha_code):
        post_data = self.booing_ticket_defualt_data
        post_data["startTime"] = ticket.start_time
        post_data["arriveTime"] = ticket.arrive_time
        post_data["trainNo"] = ticket.trn_number
        post_data["trnClassCode"] = ticket.trn_class_code
        post_data["startStationCode"] = ticket.start_station_code
        post_data["endStationCode"] = ticket.end_station_code
        post_data["adultTktPrice"] = ticket.price
        post_data["halfTktPrice"] = ticket.half_price
        post_data["customerId"] = ticket.id_card
        post_data["trainLine"] = ticket.train_line
        post_data["ptrTransferList"][0]["startStaCode"] = ticket.start_station_code
        post_data["ptrTransferList"][0]["endStaCode"] = ticket.end_station_code
        post_data["ptrTransferList"][0]["trnClassCode"] = ticket.trn_class_code
        post_data["ptrTransferList"][0]["trainNo"] = ticket.trn_number
        post_data["ptrTransferList"][0]["startDateTime"] = ticket.start_time
        post_data["ptrTransferList"][0]["endDateTime"] = ticket.arrive_time
        post_data["trnLine"] = ticket.train_line
        url = HOST + '/tra-tip-web/ptr/pts131/tktOrderNormal'

        self._setting_secret_key()
        header = self.header
        header['recaptchaToken'] = captcha_code
        r = self.session.post(url, json=[post_data], headers=header)
        ticket_info = json.loads(r.text)
        logging.info(ticket_info)
        if ticket_info["message"] == "OK":
            ticket.ticket_number = ticket_info["data"][0]["tktRecNo"]
            if ticket.ticket_number is None:
                return None
            return ticket
        else:
            return None


class TrainCrawlerTask(threading.Thread):
    def __init__(self, line_id, parm):
        super().__init__()
        self.line_id = line_id
        self.query_parm = parm
        self.start_date = datetime.now()

    def run(self):
        for i in range(20):
            time.sleep(1)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "%s" % (self.getName(),))


# print(len('a85ae71b84d2c04a7b99a9c46638364c561b26a6f4b934aef95ddd58ec9042d8'))

if __name__ == '__main__':
    train_crawler = TrainCrawler()
    ticket = train_crawler.query_exist_seat()
    # print(ticket)
    # code = train_crawler.captcha_hack()
    # if code is not None:
    #     train_crawler.booking_ticket(ticket, code)
