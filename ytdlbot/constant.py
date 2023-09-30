#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - constant.py
# 8/16/21 16:59
#

__author__ = "Benny <benny.think@gmail.com>"

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start = "مرحبا بك في بوت تنزيل الميديا العراقي !\nللأوامر والمعلومات استخدم الأمر\n/help"
    help = f"""
    يمكنك تنزيل مقاطع الفيديو من منصة اليوتيوب وبالجودة المختارة وايضا تحويل المقطع الى ملف صوتي فقط . ارسل رابط مقطع الفيديو او قائمة تشغيل لبدأ التنزيل او تحويله الى صوت فقط
    • الأوامر الاضافية •
    /settings - الاعدادات (الجودة والصيغ)
    /direct - للتنزيل من رابط مباشر وليس يوتيوب
    •المطور•
    @ri2da
    لأي مساعدة او استفسار او حدوث مشكلة يرجى ارسالها الى المطور
    """

    about = "المطور @ri2da\n لصالح قناة @iqbots0"

    buy = f"""
    البوت مجاني حالياً لتوفر خدمة استضافة مجانية
    """
    private = "This bot is for private use"
    membership_require = f"You need to join this group or channel to use this bot\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
اختر ما تريده من الاعدادات سواء الجودة او الارساب كملف.
High quality is recommended. Medium quality is 720P, while low quality is 480P.

Please keep in mind that if you choose to send the video as a document, it will not be possible to stream it.

Your current settings:
Video quality: **{0}**
Sending format: **{1}**
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"Too many tasks. Your tasks was added to the reserved queue {reserved}."
        else:
            text = "Your task was added to active queue.\nProcessing...\n\n"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
