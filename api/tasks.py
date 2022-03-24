from celery import shared_task
from api.trainCrawler.trainCrawler import *
from api.trainCrawler.entities.trainTicket import *
import logging
from datetime import datetime, timedelta
import traceback
from TrainLineBot.lineBotApi import line_bot_api
from linebot.models import TextSendMessage


@shared_task
def booking_ticket_task(user_id, id_card, train_code, start_code, end_code, start_time, end_time):
    train_crawler = TrainCrawler()
    ticket = None
    current_time = datetime.now()
    try:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        while datetime.now() < end_time and datetime.now() - current_time < timedelta(hours=24):
            try:
                ticket = train_crawler.query_exist_seat(id_card, TRAIN_CODE_MAP[train_code], start_code, end_code, start_time, end_time)
            except Exception as e:
                traceback.print_exc()
            if ticket is not None:
                line_bot_api.push_message(user_id, TextSendMessage(text=str(ticket)))
                break
            time.sleep(60)

    except QueryExistSeatException:
        logging.error("booking_ticket_task QueryExistSeatException")