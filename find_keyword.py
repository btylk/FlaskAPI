import pythainlp
import codecs
import json
from pythainlp.util import find_keyword
from pythainlp.tokenize import word_tokenize

with codecs.open('./data/data7.txt','r','utf-8') as web, codecs.open('bully_word.txt','r','utf-8') as corpus:
    sentence = web.readline()
    web_data = word_tokenize(sentence, engine="newmm",keep_whitespace=False)
    all_word = len(web_data)

    lines_corpus = corpus.readlines()
    tokens_column_number = 0
    word_corpus=[]
    for x in lines_corpus:
        word_corpus.append(x.split()[tokens_column_number])

    find = []
    for i in word_corpus:
        if i in web_data:
            find.append(i)
    all_find = len(find)

    result = float((all_find/all_word)*100)
# print(len(resulttoken))
# print(web_data)
# print('\n')
# print(word_corpus)
# print("คำทั้งหมดในข้อความ %d คำ"%all_word)
# print("คำที่พบ %s"%find)
# print("ร้อยละ %.2f"%result)

data = {'Data':[{'All_Word': all_word, 'Word_Found': find, 'Percent': result}]}
export_data = json.dumps(data,ensure_ascii=False,indent=4)
print(export_data)