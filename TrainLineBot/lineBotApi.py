from linebot import LineBotApi, WebhookHandler
from TrainLineBot import settings


line_bot_api = LineBotApi(settings.LINE_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_SECRET)
