from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from TrainLineBot.lineBotApi import line_bot_api, handler
from api.trainCrawler.trainCrawler import *
from api.commandHandler import CommandHandler
from TrainLineBot import settings
from api.strings import Strings
import traceback

logger = logging.getLogger("django")

@csrf_exempt
@require_POST
def webhook(request: HttpRequest):
    signature = request.META["HTTP_X_LINE_SIGNATURE"]
    body = request.body.decode()
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        messages = (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        logger.error(messages)
        return HttpResponseBadRequest(messages)
    return HttpResponse("OK")


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    try:
        command_handler = CommandHandler(event.source.user_id)
        replay_text = command_handler.run(event.message.text)
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text=replay_text),
        )

    except Exception as e:
        traceback.print_exc()
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text=Strings.INTRODUCTION_MESSAGE),
        )


@handler.add(MessageEvent)
def handle_message(event, destination):
    print(destination)
    print(event)
    print('貼圖之類的嗎')
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(text='喵'),
    )


@handler.default()
def default(event):
    print('default')

def index(request):
    return HttpResponse("Hello, world")

def web(request):
    return HttpResponse("Hello, web")