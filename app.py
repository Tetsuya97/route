from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

app = Flask(__name__)

ACCESS_TOKEN = "DSqCjWoRUlBWFyBRGtzTU3m0jpB/3SDMTJ5k8ChNOH958pnqVv3ACsqcymwQjaw04vQLP1WvmhZ3T10U3XjdJ6ljDwYP9awasav3ULJ6KPO42J/oZJreN6udtUz6UAJ3plPTKqGSc+SHAZWm/Os//gdB04t89/1O/w1cDnyilFU="
SECRET = "88f03e43fdde9943c2db1c017f1d61a9"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route(“/ callback”, methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] body = request.get_data(as_text=True)
    app.logger.info(“Request body: ” + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text))


if __name__ == “__main__”:
    app.run()
