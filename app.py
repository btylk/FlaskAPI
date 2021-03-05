from flask import Flask, request
from flask import jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json
import pythainlp
import codecs
from pythainlp.util import find_keyword
from pythainlp.tokenize import word_tokenize

app = Flask(__name__)
api = Api(app)
CORS(app)
@app.route('/')
def hello():
    return "hello"

@app.route('/test_post', methods=['POST','GET'])
def test_post():
	if request.method == 'POST':
		# input_value = request.form["input_value"]
		# url = input_value
		req = request.get_json()
		url = req['data']
		with codecs.open('bully.txt','r','utf-8') as bully, codecs.open('depress.txt','r','utf-8') as depress, codecs.open('desolate.txt','r','utf-8') as desolate:
			# # url = req*5
			# # url = data
			res = requests.get(url)
			res.encoding = "utf-8"
			soup = BeautifulSoup(res.text, 'html5lib')
			title = soup.title.string
			h2 = soup.h2.string	
			p_list = []
			p = soup.find_all('p')
			if(p != None):
				for data in p:
					obj = data.string
					p_list.append(obj)
			else:
				None

			#sentiment
			url = "https://api.aiforthai.in.th/ssense"
			text = title
			data = {'text':text}
			headers = {
				'Apikey': "07IC7nlLNGUsFXcERk4PoBCoL9TW7u6s"
			}
			sentiment = requests.post(url, data=data, headers=headers)
			sentiment_data = sentiment.json()
			score = sentiment_data["sentiment"]["score"]
			polarity = sentiment_data["sentiment"]["polarity"]
			sentiments = sentiment_data["intention"]["sentiment"]
			announcement = sentiment_data["intention"]["announcement"]

			#analysis with corpus		
			sentence = title
			web_data = word_tokenize(sentence, engine="newmm",keep_whitespace=False)
			all_word = len(web_data)

			# ##read corpus 
			# lines_corpus = corpus.readlines()
			# tokens_column_number = 0
			# word_corpus=[]
			# for x in lines_corpus:
			# 	word_corpus.append(x.split()[tokens_column_number])
			
			##read bully
			lines_bully = bully.readlines()
			word_bully=[]
			for x in lines_bully:
				word_bully.append(x.split()[0])

			##read depress
			lines_depress = depress.readlines()
			word_depress=[]
			for y in lines_depress:
				word_depress.append(y.split()[0])
			
			##read desolate
			lines_desolate = desolate.readlines()
			word_desolate=[]
			for z in lines_desolate:
				word_desolate.append(z.split()[0])

			# ##find 
			# find = []
			# for i in word_corpus:
			# 	if i in web_data:
			# 		find.append(i)
			# all_find = len(find) 

			##find bully
			find_bully = []
			for i in word_bully:
				if i in web_data:
					find_bully.append(i)
			all_bully = len(find_bully)

			##find depress
			find_depess = []
			for i in word_depress:
				if i in web_data:
					find_depess.append(i)
			all_depress = len(find_depess)

			##find desolate
			find_desolate = []
			for i in word_desolate:
				if i in web_data:
					find_desolate.append(i)
			all_desolate = len(find_desolate)


			result = round(float(((all_bully + all_depress + all_desolate)/all_word)*100),2)  
			word_left = (100 - result)
			data = {
				'Title': title,
				# 'H2': h2,
				'Score': score,
				'Polarity': polarity,
				'Sentiment': sentiments,
				'Announcement': announcement,
				'All_word': all_word,
				# 'Word_found': find,
				'Bully_found': find_bully,
				'Depress_found': find_depess,
				'Desolate_found': find_desolate,
				'Other_person': {
					'Bully_found': find_bully,
					'All_bully': all_bully
				},
				'Itself': {
					'Depress_found': find_depess,
					'All_depress': all_depress,
					'Desolate_found': find_desolate,
					'All_desolate': all_desolate
				},
				'Percent_found': result,
				'Percent_left': word_left
				
			}
			# if all_bully != 0:
			# 	update_bully = {'Bully_found' : find_bully}
			# 	data.update(update_bully)

		return jsonify(data)
		# return jsonify(req)
	if request.method == 'GET':
		url = "https://www.msn.com/th-th/news/national/ข่าวดีแรงงาน-ประกันสังคมแจ้งผู้รับผลกระทบโควิด-ยื่นรับสิทธิว่างงาน-ดีเดย์-4-มกราคมนี้/ar-BB1cqX4N"
		res = requests.get(url)
		res.encoding = "utf-8"
		soup = BeautifulSoup(res.text, 'html5lib')
		title = soup.title.string
		h1 = soup.h1.string
		if h1 != title:
			pass
		else:
			h1 = None	
		data = {
			'Title': title,
			'H1': h1
		}
		return jsonify(data)
	return '200'




if __name__ == "__main__":
    app.run(debug=False)