#-*- coding: utf-8 -*-
from slackbot.bot import listen_to
from datetime import datetime,timedelta
 
# 現在日時の取得
now = datetime.now()
target = datetime(2017, 8, 21, 8, 0, 0, 000000)

delta = target - now


@listen_to('院試')
@listen_to('テスト')
def cheer(message):
    message.reply('院試まであと'+str(delta).split()[0]+'日!')



#print('院試まであと'+str(delta).split()[0]+'日!')


