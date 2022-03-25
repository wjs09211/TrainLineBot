from api.utils.strings import Strings
from api.models import Station, Task
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from api.utils.exceptions import *
from api.tasks import booking_ticket_task
import traceback
import logging
from api.trainCrawler.trainCrawler import TrainCrawler
from api.trainCrawler.entities.trainTicket import TRAIN_CODE_MAP
from api.utils.status import Status
import threading


class CommandHandler:
    def __init__(self, user_id):
        self.handlers = {
            "add": self._add_handler,
            "query": self._query_handler,
            "delete": self._delete_handler
        }
        self.user_id = user_id

    def run(self, command_string):
        try:
            command = command_string.split(' ')[0]
            arg = command_string[len(command) + 1:]
            func = self.handlers.get(command, None)
            if func is None:
                raise UnknownCommandException
            return func(arg)
        except UnknownCommandException as e:
            traceback.print_exc()
            return Strings.INTRODUCTION_MESSAGE
        except Exception as e:
            traceback.print_exc()
            return Strings.INTRODUCTION_MESSAGE

    def _add_handler(self, arg):
        try:
            id_card, train_code, start_code, end_code, start_time, end_time = self._parser_order_string(arg)
        except ParserBookingInfoException as e:
            return Strings.ERROR_ADD_FORMAT
        except ParserBookingInfoStartStationException as e:
            return Strings.ERROR_ADD_FORMAT_START_STATION
        except ParserBookingInfoEndStationException as e:
            return Strings.ERROR_ADD_FORMAT_END_STATION
        except ParserBookingInfoTimeException as e:
            return Strings.ERROR_ADD_FORMAT_Time
        # test once
        try:
            train_crawler = TrainCrawler()
            ticket = train_crawler.query_exist_seat(id_card, TRAIN_CODE_MAP[train_code],
                                                    start_code, end_code, start_time, end_time)
        except QueryExistSeatException as e:
            return Strings.ERROR_QUERY_SEAT
        except Exception as e:
            traceback.print_exc()
            return Strings.ERROR_QUERY_SEAT

        # add order task
        task = Task.objects.filter(line_id=self.user_id).first()
        if task is None or task.status == Status.DELETING:
            task = Task(line_id=self.user_id, status=Status.RUNNING)
            task.save()
            t = threading.Thread(target=booking_ticket_task,
                             args=(self.user_id, id_card, train_code, start_code, end_code, start_time, end_time))
            t.start()
            # booking_ticket_task.delay(self.user_id, id_card, train_code, start_code, end_code, start_time, end_time)
            return Strings.ADD_BOOKING_TASK_SUCCESS
        else:
            return Strings.ERROR_ALREADY_HAS_TASK

    def _parser_order_string(self, string):
        # 2022/03/23-12:00
        try:
            parms = string.strip().replace(' ', '').split(',')
            if len(parms) < 6:
                raise ParserBookingInfoException
        except Exception:
            raise ParserBookingInfoException

        id_card = parms[0]
        train_code = parms[1]

        try:
            start_code = Station.objects.get(name=parms[2]).code
        except ObjectDoesNotExist:
            raise ParserBookingInfoStartStationException
        try:
            end_code = Station.objects.get(name=parms[3]).code
        except ObjectDoesNotExist:
            raise ParserBookingInfoEndStationException
        try:
            # start_time = datetime.strptime(parms[4], "%Y/%m/%d-%H:%M").strftime("%Y-%m-%d %H:%M:%S")
            # end_time = datetime.strptime(parms[5], "%Y/%m/%d-%H:%M").strftime("%Y-%m-%d %H:%M:%S")
            start_time = datetime.strptime(parms[4], "%Y/%m/%d-%H:%M")
            end_time = datetime.strptime(parms[5], "%Y/%m/%d-%H:%M")

            if start_time > end_time or datetime.now() > end_time:
                logging.error("error time interval")
                raise ParserBookingInfoTimeException
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            logging.error("error time format")
            raise ParserBookingInfoTimeException
        return id_card, train_code, start_code, end_code, start_time, end_time

    def _query_handler(self, arg):
        task = Task.objects.filter(line_id=self.user_id).first()
        if task is not None:
            if task.status == Status.RUNNING:
                return Strings.QUERY_BOOKING_TASK_RUNNING
        else:
            return Strings.QUERY_BOOKING_TASK_NO_TASK

    def _delete_handler(self, arg):
        task = Task.objects.filter(line_id=self.user_id).first()
        if task is not None:
            Task.objects.filter(line_id=self.user_id).delete()
            return Strings.DELETE_BOOKING_TASK_SUCCESS
        else:
            return Strings.QUERY_BOOKING_TASK_NO_TASK



if __name__ == "__main__":
    CommandHandler.run("add test")
