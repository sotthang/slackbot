import os
import random
import requests
import datetime
import calendar
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Callable
from datetime import time, date
from bs4 import BeautifulSoup
from flask import Flask, request
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler

'''
slackbottoken = open("token_sotthang.txt", "r").readline()
slacksigningtoken = open("token_sotthang_signing.txt", "r").readline()
'''
# env
slackbottoken = open("token_lupin.txt", "r").readline()
slacksigningtoken = open("token_lupin_signing.txt", "r").readline()
os.environ['SLACK_BOT_TOKEN'] = slackbottoken
os.environ['SLACK_SIGNING_SECRET'] = slacksigningtoken
client = WebClient(token=slackbottoken)
logger = logging.getLogger(__name__)

# flask
flask_app = Flask(__name__)

# bolt
app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# mention 기능
def mention_handler(body: dict, say: Callable):
	print(body)

# 요일 계산
def getdays(yyyy, mm, dd):
	return datetime.date(yyyy, mm, dd).weekday()

# 날씨 크롤링
def weather():
	html1 = requests.get('https://weather.naver.com/today')
	soup = BeautifulSoup(html1.text, 'html.parser')
	post = soup.find('strong',{'class':'current'}).text
	minimum = soup.find('span',{'class':'lowest'}).text
	maximum = soup.find('span',{'class':'highest'}).text
	
	html2 = requests.get('https://www.weather.go.kr/w/weather/forecast/short-term.do')
	soup2 = BeautifulSoup(html2.text, 'html.parser')
	total = soup2.find('span',{'class':'depth_1'}).text
	today = soup2.find('span',{'class':'depth_2'}).text
	
	return(post + "\n" + "최저 " + minimum[4:] + "\n" + "최고 " + maximum[4:] + "\n" + "\n" + total + "\n" + today)

# blocks 참고
'''
@app.message("hello")
def message_hello(message, say):
	say(
		blocks=[
			{
				"type": "section",
				"text": {"type": "mrkdwn", "text": f"hello <@{message['user']}>!"},
				"accessory": {
					"type": "button",
					"text": {"type": "plain_text", "text": "Click Me"},
					"action_id": "button_click"
				}
			}
		],
		text=f"Hey there <@{message['user']}>!"
	)


@app.action("button_click")
def action_button_click(body, ack, say):
	# Acknowledge the action
	ack()
	say(f"<@{body['user']['id']}> clicked the button")
'''

# mention 실행
@app.event("app_mention")
def mention_handler(body: dict, say: Callable):
	bot_id = body.get("event", {}).get("text").split()[0]
	message = body.get("event", {}).get("text")
	message = message.replace(bot_id, "").strip()
	# say(message)
	if message == "명령어":
		say("나무위키 : 나무위키 검색 (ex: 나무위키 나루)\n유튜브 : 유튜브 검색 (ex: 유튜브 나루)\n주사위 : 주사위 굴리기 (ex: 주사위 6 -> 1부터 6까지의 숫자 중 하나 랜덤 출력)\n골라줘 : 하나 고르기 (ex: 골라줘 짜장 짬뽕)\n월급날 : 월급날 언제인지\n날씨 : 현재 날씨\n")
	elif message[:4] == "나무위키":
		namu_command1 = message[5:]
		namu_command2 = namu_command1.replace(" ","%20")
		say("https://namu.wiki/w/" + namu_command2)
	elif message[:3] == "유튜브":
		youtube_command1 = message[4:]
		youtube_command2 = youtube_command1.replace(" ","+")
		say("https://www.youtube.com/results?search_query=" + youtube_command2)
	elif message[:3] == "주사위":
		dice = message.split()
		say(str(random.randint(1,int(dice[1]))) + " (이)다냥")
	elif message[:3] == "골라줘":
		choose1 = message.split()
		choose = choose1[1:]
		choose1 = set(choose)
		if len(choose1) == 1:
			say("답정너다냥 :naru_5")
		else:
			say(random.choice(choose) + " (이)다냥")
	elif message == "월급":
		today = date.today()
		yyyy = today.year
		mm = today.month
		dd = calendar.monthrange(today.year, today.month)[1]
		if getdays(yyyy, mm, dd) == 5:
			dd = dd - 1
		elif getdays(yyyy, mm, dd) == 6:
			dd = dd - 2
		diff_day1 = datetime.date(yyyy, mm, dd) - today # 월말 월급 날 계산

		twentyfive_day = datetime.date(today.year, today.month, 25) # 이번 달 25일
		yyyy1 = twentyfive_day.year
		mm1 = twentyfive_day.month
		dd1 = twentyfive_day.day
		if getdays(yyyy1, mm1, dd1) == 5:
			dd1 = dd1 - 1
		elif getdays(yyyy1, mm1, dd1) == 6:
			dd1 = dd1 - 2
		diff_day2 = datetime.date(yyyy1, mm1, dd1) - today # 25일 월급 날 계산

		if diff_day1.days == 0:
			say("31일 월급 날이다냥!\n" + "25일 월급은 이미 받았다냥:naru_5:")
		elif diff_day2.days == 0:
			say("25일 월급 날이다냥!\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:")
		elif diff_day1.days > 0 and diff_day2.days < 0:
			say("25일 월급은 이미 받았다냥\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:")
		elif diff_day1.days < 0 and diff_day2.days < 0:
			say(str(mm) + "월 월급은 이미 받았다냥 다음 달 월급을 기다리라냥")
		else:
			say(str(mm) + "월 월급\n" + "25일 월급은 " + str(diff_day2.days) + "일\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:")
	elif message == "날씨":
		say(weather())
	else:
		say(message + "는 없으니 명령어를 입력해냥 :naru_4:")

# conversation read
@app.message("그래서 뭐먹")
def say_hello(say):
	menu = ['초밥', '덮밥', '국밥', '피자', '햄버거', '삼겹살', '중국집', '분식', '곱창']
	say(random.choice(menu))

@app.message("나루")
def say_hello(say):
	naru = [':naru_1:', ':naru_2:', ':naru_3:', ':naru_4:', ':naru_5:', ':naru_6:', ':naru_7:']
	say(random.choice(naru))

# post message
'''
try:
	response = client.chat_postMessage(
		channel="C026SF30S79",
		text="test"
	)
except SlackApiError as e:
	assert e.response["error"]'''

# scheduler
'''
try:
	today = datetime.date.today()
	scheduled_time = datetime.time(hour=13, minute=9)
	schedule_timestamp = datetime.datetime.combine(today, scheduled_time).strftime('%s')
	print(schedule_timestamp)

	# Call the chat.scheduleMessage method using the WebClient
	result = client.chat_scheduleMessage(
		channel="C026SF30S79",
		text="scheduler test",
		post_at=schedule_timestamp
	)
	# Log the result
	logger.info(result)

except SlackApiError as e:
	logger.error("Error scheduling message: {}".format(e))
'''


handler = SlackRequestHandler(app)

# flask
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
	return handler.handle(request)

if __name__ == "__main__":
	flask_app.run(host='0.0.0.0', port=8080)
	# flask_app.run(host='0.0.0.0', port=8080, debug=True)
