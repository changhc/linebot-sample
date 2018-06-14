from flask import Flask, request, make_response, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage
)
import json
import requests

def main():
    app = Flask(__name__)
    with open('../.config') as file:
        message_url = file.readline().strip()
        channel_access_token = file.readline().strip()
        channel_secret = file.readline().strip()
    
    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)

    @app.route('/api/message', methods=['POST'])
    def callback():
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        print(event)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

    @handler.add(MessageEvent, message=StickerMessage)
    def handle_message(event):
        print(event.message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='You sent a sticker with id %s' %
                (event.message.sticker_id))) #

    @app.route("/")
    def hello():
        return "Hello World!"

    return app

if __name__ == '__main__':
    app = main()
    app.run(host='0.0.0.0', port=9000)
