from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
import os
import json

app = Flask(__name__)
app.debug = False

line_bot_api = LineBotApi(LINE_CHANNEL_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SERIAL)

@app.route("/get_mail", methods=['POST'])
def get_jeson():
    group_id = "ひみつ♡"
    mail_body = request.data.decode('utf-8')

    slice1 = mail_body.find("Ｉ２")
    slice2 = mail_body.find("----")
    mail_body = mail_body[slice1:slice2]
    print(mail_body)

    messages = TextSendMessage(text=mail_body)
    line_bot_api.push_message(group_id, messages=messages)

@app.route("/test", methods=['GET'])
def test():
    group_id = "ひみつ♡"

    messages = TextSendMessage(text="テスト：GET通信：テスト成功")
    line_bot_api.push_message(group_id, messages=messages)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.type == "message":
        if (event.message.text == "Check: GroupID"):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=event.source.group_id)
                ]
            )
        if (event.message.text == "月曜日"):
            mess = "月曜日の時間割は以下の通りです。\n1-2: EC\n3-4: 微分積分\n5-6: 歴史\n7-8: 国語\n授業変更の可能性があります。必ず確認しましょう。"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mess)
                ]
            )
        if (event.message.text == "火曜日"):
            mess = "火曜日の時間割は以下の通りです。\n1-2: EE\n3-4: 理科\n5-6: 物理\n授業変更の可能性があります。必ず確認しましょう。"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mess)
                ]
            )
        if (event.message.text == "水曜日"):
            mess = "水曜日の時間割は以下の通りです。\n1-2: 微分積分\n3-4: 代数幾何\n5-6: 一般基礎教育\n7: HR\n授業変更の可能性があります。必ず確認しましょう。"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mess)
                ]
            )
        if (event.message.text == "木曜日"):
            mess = "木曜日の時間割は以下の通りです。\n1-2: 工学数理基礎\n3-4: 保健体育\n5-8: プログラミング\n授業変更の可能性があります。必ず確認しましょう。"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mess)
                ]
            )
        if (event.message.text == "金曜日"):
            mess = "金曜日の時間割は以下の通りです。\n1-4: 電気電子工学\n5-6: EC\n授業変更の可能性があります。必ず確認しましょう。"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mess)
                ]
            )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)