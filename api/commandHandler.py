from api.strings import Strings
from api.models import Station
from datetime import datetime
from api.exceptions import *
from api.tasks import booking_ticket_task
import traceback


class CommandHandler:
    def __init__(self, user_id):
        self.handlers = {
            "add": self._add_handler
        }
        self.user_id = user_id

    def run(self, command_string):
        command = command_string.split(' ')[0]
        arg = command_string[len(command) + 1:]
        func = self.handlers.get(command, None)
        if func is not None:
            return func(arg)
        raise UnknownCommandException

    def _add_handler(self, arg):
        try:
            id_card, train_code, start_code, end_code, start_time, end_time = self._parser_order_string(arg)
        except Exception as e:
            traceback.print_exc()
            raise ParserBookingInfoException
        booking_ticket_task.delay(self.user_id, id_card, train_code, start_code, end_code, start_time, end_time)
        return Strings.ADD_BOOKING_TASK_SUCCESS

    def _parser_order_string(self, string):
        # 2022/03/23-12:00
        parms = string.strip().replace(' ', '').split(',')
        id_card = parms[0]
        train_code = parms[1]
        start_code = Station.objects.get(name=parms[2]).code
        end_code = Station.objects.get(name=parms[3]).code
        start_time = datetime.strptime(parms[4], "%Y/%m/%d-%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(parms[5], "%Y/%m/%d-%H:%M").strftime("%Y-%m-%d %H:%M:%S")
        return id_card, train_code, start_code, end_code, start_time, end_time


if __name__ == "__main__":
    CommandHandler.run("add test")
