from csv import reader
import nltk
from PIL import Image, ImageTk
from nltk.corpus import stopwords
from nltk.stem import   WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import collections
import tinysegmenter
import re
import numpy as np
import sys
from collections import Counter
from datetime import datetime
import pandas as pd


"""
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
"""

"""
preliminary variables needed to extract info here it is french but upon 
your txt file please adapt the days of the week in conversation language. 
"""
 
days_date=['lun. [0-9|/]+', 'mar. [0-9|/]+', 'mer. [0-9|/]+', 'jeu. [0-9|/]+', 'ven. [0-9|/]+', 'sam. [0-9|/]+', 'dim. [0-9|/]+'] 
vid_pics=[r'\[Photo]',r'\[Vidéo]']
emojis=[r'\🙂', r'\😌',r'\😄',r'\👍', r'\😊', r'\😀', r'\🙇',r'\😂', r'\😓',r'\😅', r'\😆', r'\🙌', r'\🙏', r'\👌',r'\🙇‍♀️', 
r'\😵',r'\🤔',r'\😥', r'\✌️',r'\😮', r'\😉', r'\💪', r'\😋', r'\😴',r'\😱', r'\😶',r'\😇', r'\👏🏼',r'\😏', r'\🌞', r'\🇫🇷', 
r'\☺️', r'\😈',r'\😳', r'\🤣',r'\😰', r'\😪', r'\☹️', r'\🤞']


date_pattern=re.compile('|'.join(days_date))
vid_pics_pattern=re.compile('|'.join(vid_pics))
emojis_pattern=re.compile('|'.join(emojis))



sender1 = '北岡 有以'
warabi = 'ファラビ (ワラビ)'

#Function that loads the conversation from a txt file. no need to use the specific tags \n and \t for
#Line as the readlines functions already split correctly the conversations line by line for other SNS apps
#The use of the tags \n and \t might be needed (I guess). 
def conversation_load():
    file = open('[LINE] Chat avec 北岡 有以.txt', 'r')
    if file.mode=='r':
        content=file.readlines()
    for line in content:
    	if line=='\n': 
    		content.remove(line)
    return content[2:]


class conversation:
	def __init__(self, conversation, sender1, sender2):
		self.conversation = conversation 
		self.sender1=sender1  
		self.sender2=sender2

#Function that merges days and time in order to reduce size of the list we'll analyze. 	
	def days_merge(self): 
		days_merge=[]
		i=0
		while i < len(self.conversation):
			if date_pattern.match(self.conversation[i]):
				days_merge.append(''.join(self.conversation[i]+self.conversation[i+1]))
				i+=2
			else:
				days_merge.append(self.conversation[i])
				i+=1
		for index in range(len(days_merge)):
			if not re.match(date_pattern,days_merge[index]):
				days_merge[index]= re.match(date_pattern,days_merge[index-1])[0]+'\n'+days_merge[index]
		return days_merge	 

#Function that cleans the conversation 
	def clean_conversation(self):
		for line in conversation.days_merge(self):
			line.strip()
		result =[( i.split("\n")[0].split('.')[0].strip(), i.split("\n")[0].split('.')[1].strip(),i.split("\n")[1].split("\t")[0].strip(), i.split("\n")[1].split("\t")[1].strip(), i.split("\n")[1].split("\t")[2].strip())  for i in conversation.days_merge(self) ]
		result=pd.DataFrame(data=result , columns=['Day','Date','Time','Sender','Content'])
		return result


#function that gives split conversation with only from one sender to the other
#in order to clean from multiple messages from one spe2cific sender in a row.
#the function return a list of tuple with first element of the tuple the message from sender 1
#and the second element of the tuple the message sent by sender 2. 
	

	def strict_reply_pd(self):
		df=conversation.clean_conversation(self)
		sender1_strict_reply= df.loc[(df['Sender'] == sender1) & (df['Sender'].shift(1)==warabi)]
		warabi_strict_reply=df.loc[(df['Sender'] == warabi) & (df['Sender'].shift(1)==sender1)]
		if df.iloc[0]['Sender']==sender1:
			result= sender1_strict_reply.combine_first(warabi_strict_reply)
		else:
			result= warabi_strict_reply.combine_first(sender1_strict_reply)   
		return result

#functions that gives the time at which the message was sent. 
	def response_time_between_messages(self, sender)-> list:
		df=conversation.strict_reply_pd(self)
		List=list(df['Date']+df['Time'])
		List = [datetime.strptime(time , '%d/%m/%Y%H:%M') for time in List]
		if df.iloc[0]['Sender']==sender1:
			response_sender1=[List[i+1]-List[i] for i in range(1, len(List)-1, 2)]
			response_sender2=[List[i+1]-List[i] for i in range(0, len(List)-1, 2)]
		if df.iloc[0]['Sender']==warabi:
			response_sender2=[ List[i+1]-List[i] for i in range(1, len(List)-1, 2)]
			response_sender1=[ List[i+1]-List[i] for i in range(0, len(List)-1, 2)]
		if sender==sender1:
			return [response.seconds for response in response_sender1]
		if sender==warabi:
			return [response.seconds for response in response_sender2]

#function that select message from a specific sender and return a string. 
	def sender_messages(self, sender)->str:
		df=conversation.clean_conversation(self)
		return ''.join(string for string in list(df.loc[df['Sender']==sender]['Content']))


#function that gives the length of each messages from a specific sender. 
	def message_length(self, data,sender)->list: 
		df=data
		return [len(element) for element in list(df.loc[df['Sender']==sender]['Content'])]

#function that provides the number of message from a specific sender. 
	def sender_number_of_message(self, sender)->int:
		df=conversation.clean_conversation(self)
		return len(list(df.loc[df['Sender']==sender]['Content']))

#function that provides the time at which messages was sent in the form of a list. 
	def msg_time(self,sender)-> dict:
		df=conversation.clean_conversation(self)
		return dict(sorted(Counter([element for element in list(df.loc[df['Sender']==sender]['Time'])]).items()))
	
#function that gives dates at which messages was sent in the form of dictionnary. 
	def msg_date(self,sender)-> dict:
		df=conversation.clean_conversation(self)
		return Counter([element for element in list(df.loc[df['Sender']==sender]['Date'])])

#function that return days at which messages was sent in the form of dictionnary. 
	def msg_days(self, sender)->dict:
		df=conversation.clean_conversation(self)
		return Counter([element for element in list(df.loc[df['Sender']==sender]['Day'])])

#function that gives the number of videos and photos sent in the form if dictionary 
	def videos_photos(self, sender)->dict:
		return Counter(re.findall(vid_pics_pattern,conversation.sender_messages(self, sender=sender)))

	def emojis(self, sender)->dict:
		return Counter(re.findall(emojis_pattern,conversation.sender_messages(self, sender=sender)))


#function that gives the frequency of word use in a string. 	
	def frequency_dict(self, string) -> dict:
		assert type(string) == str, 'You must use string in frequency_dict function'
		segmenter = tinysegmenter.TinySegmenter()
		stop_words = set(stopwords.words())
		words = segmenter.tokenize(string)
		wl = WordNetLemmatizer()
		frequency_dict = dict()
		for wd in words:
			rootword = wl.lemmatize(wd)
			if rootword in stop_words:
				continue
			elif rootword in frequency_dict:
				frequency_dict[rootword] += 1
			else:
				frequency_dict[rootword] = 1
		return sorted(frequency_dict.items(), key=lambda x: x[1])




#LINE_talk= conversation(conversation=conversation_load(), sender1=sender1, sender2=warabi)




if __name__ == '__main__':
	conversation_load()
	conversation(conversation=conversation_load(), sender1=sender1, sender2=warabi)


