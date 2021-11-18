import json
import requests
import datetime
import random
from datetime import time, date
from flask import Flask, request, make_response
from bs4 import BeautifulSoup

token = open("token_lupin.txt", "r").readline()

app = Flask(__name__)

def getdays(yyyy, mm, dd): # 요일 구하기
    return datetime.date(yyyy, mm, dd).weekday()

def post_message(token, channel, text):
	response = requests.post("https://slack.com/api/chat.postMessage",
		headers={"Authorization": "Bearer "+token},
		data={"channel": channel,"text": text}
	)
	print(response)

def get_answer_Mention(b):
	query = b.lstrip()
	command1 = ['명령어', '나무위키', '유튜브', '인스타', '주사위', '골라줘', '가위바위보', '맞춤법', '유머글', '노션', '월급', '날씨'] # 명령어
	
	if query == command1[0]: # 명령어 리스트
		return (command1[1] + " : 나무위키 검색 (ex: 나무위키 나루)\n" + command1[2] + " : 유튜브 검색 (ex: 유튜브 나루)\n"
		+ command1[3] + " : 나루의 인스타\n"+ command1[4] + " : 주사위 굴리기 (ex: 주사위 6 -> 1부터 6까지의 숫자 중 하나 랜덤 출력)\n"
		+ command1[5] + " : 하나 고르기 (ex: 골라줘 짜장 짬뽕)\n"+ command1[6] + " : 가위바위보 (ex:가위바위보 가위)\n"
		+ command1[8] + " : 인터넷 유머글 (ex: 유머글1, (유머글1 : 오유 베스트게시글 / 유머글2 : 루리웹 많이 본 글 / 유머글3 : 클리앙 추천글 게시판))\n"
		+ command1[10] + " : 월급날 언제인지\n")
	
	elif command1[1] in query: # 나무위키
		namu_command = query[5:]
		namu_command2 = namu_command.replace(" ","%20")
		return "https://namu.wiki/w/" + namu_command2
	
	elif command1[2] in query: # 유튜브
		youtube_command = query[4:]
		youtube_command2 = youtube_command.replace(" ","+")
		return "https://www.youtube.com/results?search_query=" + youtube_command2
	
	elif query == command1[3]: # 나루 인스타
		return "https://www.instagram.com/nyang.naru/"
	
	elif command1[4] in query: # 주사위
		dice = query.split()
		return str(random.randint(1,int(dice[1]))) + " (이)다냥"
	
	elif command1[5] in query: # 골라줘
		choose1 = query.split()
		choose = choose1[1:]
		choose1 = set(choose)
		if len(choose1) == 1:
			return "답정너냥 :naru_5:"
		else:
			return random.choice(choose) + " (이)다냥"
	
	elif command1[6] in query: # 가위바위보
		rps_command = query[6:]
		naru_rps2 = ['가위', '바위', '보']
		naru_rps = random.choice(naru_rps2)
		if rps_command == "가위" and naru_rps == "바위":
			return "나루는 :fist: \n나루가 이겼다냥"
		elif rps_command == "가위" and naru_rps == "보":
			return "나루는 :hand: \n나루가 졌다냥"
		elif rps_command == "바위" and naru_rps == "가위":
			return "나루는 :v: \n나루가 졌다냥"
		elif rps_command == "바위" and naru_rps == "보":
			return "나루는 :hand: \n나루가 이겼다냥"
		elif rps_command == "보" and naru_rps == "가위":
			return "나루는 :v: \n나루가 이겼다냥"
		elif rps_command == "보" and naru_rps == "바위":
			return "나루는 :fist: \n나루가 졌다냥"
		elif rps_command == naru_rps:
			return naru_rps + " 비겼다냥"
		else:
			return "잘못 입력했다냥"
	
	elif command1[8] in query: # 유머글
		if query == '유머글1':
			html = requests.get('http://www.todayhumor.co.kr/board/list.php?table=bestofbest')
			soup = BeautifulSoup(html.text, 'html.parser')
			post = soup.find_all('td',{'class':'subject'})
			post_return = "오유 베스트 게시물 10개를 가져왔다냥 :feet:\n\n"
			count = 0
			for i in post:
				post1 = i.find('a')
				link = post1.attrs["href"]
				title = post1.text
				post_return += "<http://www.todayhumor.co.kr"+ link +"|"+ title +">\n"
				count += 1
				if count == 9:
					break
			return (post_return)
		elif query == '유머글2':
			html = requests.get('https://bbs.ruliweb.com/best/selection')
			soup = BeautifulSoup(html.text, 'html.parser')
			post = soup.find_all('td',{'class':'subject'})
			post_return = "루리웹 조회수 높은 게시물 10개를 가져왔다냥 :feet:\n\n"
			count = 0
			for i in post:
				post1 = i.find('a')
				link = post1.attrs["href"]
				title = post1.text
				post_return += "<"+ link +"|"+ title +">\n"
				count += 1
				if count == 9:
					break
			return (post_return)
		elif query == '유머글3':
			html = requests.get('https://www.clien.net/service/recommend')
			soup = BeautifulSoup(html.text, 'html.parser')
			post = soup.find_all('div',{'class':'list_title'})
			post_return = "클리앙 추천 게시물 10개를 가져왔다냥 :feet:\n\n"
			count = 0
			for i in post:
				post1 = i.find('a')
				post3 = post1.find('span', {'class':'subject_fixed'})
				link = post1.attrs["href"]
				title = post3.attrs["title"]
				post_return += "<https://www.clien.net"+ link +"|"+ title +">\n"
				count += 1
				if count == 9:
					break
			return (post_return)
		else:
			return "*유머글1* 또는 *유머글2* 또는 *유머글3* 을 입력해라냥"
	
	elif command1[10] in query: # 월급
		today = date.today()
		last_day = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1) # 이번 달 마지막 날
		yyyy = last_day.year
		mm = last_day.month
		dd = last_day.day
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
			return "31일 월급 날이다냥!\n" + "25일 월급은 이미 받았다냥:naru_5:"
		elif diff_day2.days == 0:
			return "25일 월급 날이다냥!\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:"
		elif diff_day1.days > 0 and diff_day2.days < 0:
			return "25일 월급은 이미 받았다냥\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:"
		elif diff_day1.days < 0 and diff_day2.days < 0:
			return str(mm) + "월 월급은 이미 받았다냥 다음 달 월급을 기다리라냥"
		else:
			return str(mm) + "월 월급\n" + "25일 월급은 " + str(diff_day2.days) + "일\n" + "31일 월급은 " + str(diff_day1.days) + "일 남았다냥 :naru_4:"
	
	elif command1[11] in query: # 날씨
		html1 = requests.get('https://weather.naver.com/today')
		soup = BeautifulSoup(html1.text, 'html.parser')
		post = soup.find('strong',{'class':'current'}).text
		dust = soup.find('em',{'class':'level_text'}).text
		minimum = soup.find('span',{'class':'lowest'}).text
		maximum = soup.find('span',{'class':'highest'}).text
		
		html2 = requests.get('https://www.weather.go.kr/w/weather/forecast/short-term.do')
		soup2 = BeautifulSoup(html2.text, 'html.parser')
		total = soup2.find('span',{'class':'depth_1'}).text
		today = soup2.find('span',{'class':'depth_2'}).text
		
		return post + "\n" + "최저 " + minimum[4:] + "\n" + "최고 " + maximum[4:] + "\n" + "미세먼지 " + dust + "\n" + total + "\n" + today
	
	elif ('출근' in query) or ('빨빨출' in query): # 출근
		now = datetime.datetime.now()
		today10am = now.replace(hour=10, minute=0, second=0)
		diff_time1 = today10am - now
		if now < today10am:
			return "출근까지 " + str(diff_time1) + " 남았다냥"
		else:
			return "출근 안하고 뭐했냥 :naru_4:"
	
	elif ('퇴근' in query) or ('빨빨퇴' in query): # 퇴근
		now = datetime.datetime.now()
		today19am = now.replace(hour=19, minute=0, second=0)
		diff_time2 = today19am - now
		if now < today19am:
			return "퇴근까지 " + str(diff_time2) + " 남았다냥"
		else:
			return "퇴근 하라냥! :naru_5:"
	else: # 명령어에 없을 경우
		return query + " 은(는) 없으니 *명령어* 를 입력해냥 :naru_4:"

def get_answer_channel_Message(a):
	query = a.lstrip()
	naru = []
	command = ['나루'] # 명령어
	if query == command[0]: # 나루
		naru = [':naru_1:', ':naru_2:', ':naru_3:', ':naru_4:', ':naru_5:', ':naru_6:', ':naru_7:']
		return random.choice(naru)
	elif query == '그래서 뭐먹':
		lunch = ['초밥', '덮밥', '국밥', '피자', '햄버거', '삼겹살', '중국집', '분식', '곱창']
		return random.choice(lunch)

def event_handler(event_type, slack_event):
	channel = slack_event["event"]["channel"]
	user_id = slack_event["event"]
	#ts = slack_event["event"]["ts"]
	
	if event_type == "app_mention": # 멘션으로 호출에 대해 반응
		try:
			user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
			answer = get_answer_Mention(user_query)
			post_message(token,channel,answer)
			return make_response("ok", 200)
		except IndexError:
			pass
		except KeyError:
			pass
	elif event_type == "message" and user_id != "botID": # 채널 모든 메시지에 대해 반응
		try:
			user_query = slack_event['event']['text']
			answer = get_answer_channel_Message(user_query)
			post_message(token,channel,answer)
			# post_message(token,channel,user_id) # user_id 알아내기
			return make_response("ok", 200, )
		except IndexError:
			pass
		except KeyError:
			pass
		
	message = "[%s] cannot find event handler" % event_type
	return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route('/', methods=['POST'])
def hello_there():
	slack_event = json.loads(request.data)
	if "challenge" in slack_event:
		return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
	if "event" in slack_event:
		event_type = slack_event["event"]["type"]
		return event_handler(event_type, slack_event)
	return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})

if __name__== "__main__":
	app.run(host="192.168.50.10", port=9999)
