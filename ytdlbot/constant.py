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
    كما يمكنك البحث في اليوتيوب عبر ارسال نص البحث فقط وسيتم إرسال نتائج البحث
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
    private = "البوت للاستخدام الشخصي"
    membership_require = f"يجب ان تنظم الى القناة لاستخدام البوت\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"
    
    settings = """
 اختر ما تريده من الاعدادات مقدار الجودة او نوع الإرسال

الجودة العالية موصاة بها. الجودة المتوسطة بدقة 720 اما الضعيفه بدقة 480

ملاحظة: اذا اخترت إرسال الفيديو كملف لن يمكنك مشاهدته قبل تنزيله كاملاً (لن يعمل كبث)
:اعداداتك الحالية
**{0}** :جودة الفيديو
**{1}** :صيغة الإرسال
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"{reserved} هنالك عمليات كثيرة تم وضعك في الطابور برقم."
        else:
            text = "تم اضافة العملية\nجاري التنزيل...\n\n"

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
