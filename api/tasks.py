# from celery import shared_task
from api.trainCrawler.trainCrawler import *
from api.trainCrawler.entities.trainTicket import *
import logging
from datetime import datetime, timedelta
import traceback
from TrainLineBot.lineBotApi import line_bot_api
from linebot.models import TextSendMessage
from api.models import Task
from api.utils.status import Status

# @shared_task
def booking_ticket_task(user_id, id_card, train_code, start_code, end_code, start_time, end_time):
    train_crawler = TrainCrawler()
    ticket = None
    current_time = datetime.now()
    start_time_str = start_time
    end_time_str = end_time
    try:
        time.sleep(5)
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        # 最長執行24小時
        while datetime.now() < end_time and datetime.now() - current_time < timedelta(hours=24):
            try:
                task = Task.objects.filter(line_id=user_id).first()
                if task is None or task.status == Status.DELETING:
                    break
                logging.info(user_id + " query_exist_seat!")
                ticket = train_crawler.query_exist_seat(id_card, TRAIN_CODE_MAP[train_code], start_code, end_code, start_time_str, end_time_str)
                if ticket is not None:
                    line_bot_api.push_message(user_id, TextSendMessage(text="搜尋到剩餘車位，嘗試為您自動訂票:\n" + str(ticket)))
                    code = train_crawler.captcha_hack()
                    if code is not None:
                        ticket = train_crawler.booking_ticket(ticket, code)
                        if ticket is not None and ticket.ticket_number is not None:
                            line_bot_api.push_message(user_id, TextSendMessage(text="成功訂到票了:\n" + str(ticket)))
                            break
                        else:
                            line_bot_api.push_message(user_id, TextSendMessage(text="訂票失敗，持續為您訂票"))
                    else:
                        line_bot_api.push_message(user_id, TextSendMessage(text="訂票失敗(驗證碼)，持續為您訂票"))
            except NoMoneyException as e:
                line_bot_api.push_message(user_id, TextSendMessage(text="驗證碼辨識功能沒錢了 995"))
                break
            except Exception as e:
                traceback.print_exc()
                # line_bot_api.push_message(user_id, TextSendMessage(text="訂票失敗"))
                break
            time.sleep(10)

    except Exception:
        traceback.print_exc()
        logging.error("booking_ticket_task QueryExistSeatException")

    finally:
        Task.objects.filter(line_id=user_id).delete()


def add(i):
    while i > 0:
        i-=1
        print(i)
        time.sleep(5)
