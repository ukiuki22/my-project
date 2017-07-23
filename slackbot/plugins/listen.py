#-*- coding: utf-8 -*-
from slackbot.bot import listen_to,respond_to

@respond_to(' ')
def heer(message):
    message.reply('Hello!')
    
@listen_to('疲れた')
@listen_to('つかれた')
def cheer(message):
    message.reply('がんばれ．')

@listen_to('お疲れ')
@listen_to('おつかれ')
def cheer(message):
    message.reply('おつかれ〜')


@listen_to('進捗')
def cheer(message):
        message.reply('進捗は降ってこないよ．')

@listen_to('りょうかい')
@listen_to('了解')
def gotit(message):
    message.reply('+1')
