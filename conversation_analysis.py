from Line_analysis import *
import numpy as np



##################################################
"""
Element to analyze:

################Conversation as a whole#####################

-The number of messages per sender. 
-regrouper les deux messages et non le message. 
-The most frequent time at which the sender send messages. 
-The most frequent day at which the sender send messages. 
-The frequency of word sent for each sender. 
-The average length of messages per sender. 
-The longest time between 2 reponses. 
-The longest message per sender. 
-number of relance for each sender. difficile 
-Length of the concatenation of message per sender. 
-The number of photos and videos per sender. 
-number of emojis. most often used emoji
-exclamation, interoggation points.
-message per day. 
-lexical diversity per sender. len of dictionary. 
-number of calls and lenght of the call. 
-The average response time per sender for strict reply. graph par paquet de 100 messages. 
-The frequency of word for direct reply from each sender. 
-The average length of messages for direct reply for each sender.

"""
################Diversion between senders result#############



################Normalized studied###########################
"""
more messages from warabi than from sender1 so we need to use a 
normalization coefficient
normalization_ratio=Warabi_number_of_message/sender1_number_of_message
"""

LINE_talk= conversation(conversation=conversation_load(), sender1=sender1, sender2=warabi)


clean_dataframe=LINE_talk.clean_conversation()

strict_reply_dataframe=LINE_talk.strict_reply_pd()



sender1_messages= LINE_talk.sender_messages(sender=sender1)
Warabi_messages= LINE_talk.sender_messages(sender=warabi)

#The number of messages per sender. 
sender1_number_of_message= LINE_talk.sender_number_of_message(sender=sender1)
Warabi_number_of_message= LINE_talk.sender_number_of_message(sender=warabi)

#number of videos and photos shared per sender
vid_photos_warabi=LINE_talk.videos_photos(sender=warabi)
vid_photos_sender1=LINE_talk.videos_photos(sender=sender1)

#number of emojis and type of emojis shared by each sender
emojis_warabi=LINE_talk.emojis(sender=warabi)
emojis_sender1=LINE_talk.emojis(sender=sender1)

#The most frequent time at which the sender send messages
Msg_time_sender1=LINE_talk.msg_time(sender=sender1)
Msg_time_Warabi=LINE_talk.msg_time(sender=warabi)

#The most frequent day at which the sender send messages. 
Msg_days_sender1= LINE_talk.msg_days(sender=sender1)
Msg_days_Warabi= LINE_talk.msg_days(sender=warabi)

#The frequency of word sent for each sender.
Word_frequency_sender1=LINE_talk.frequency_dict(sender1_messages)
Word_frequency_Warabi=LINE_talk.frequency_dict(Warabi_messages)

#Length of messages per sender
length_sender1=LINE_talk.message_length(data=clean_dataframe, sender=sender1)
length_warabi=LINE_talk.message_length(data=clean_dataframe, sender=warabi)

#Length of messages per sender strict reply
length_sender1_strict=LINE_talk.message_length(data=strict_reply_dataframe , sender=sender1)
length_warabi_strict=LINE_talk.message_length(data=strict_reply_dataframe , sender=warabi)

#Date at which the message was sent per sender
msg_date_warabi=LINE_talk.msg_date(sender=warabi)
msg_date_sender1=LINE_talk.msg_date(sender=sender1)

#response time per sender
response_time_warabi=LINE_talk.response_time_between_messages(sender=warabi)
response_time_sender1=LINE_talk.response_time_between_messages(sender=sender1)

normalization_ratio=Warabi_number_of_message/sender1_number_of_message
"""

print(dict(sorted(Counter(length_sender1).items())),np.mean(length_sender1))
print(dict(sorted(Counter(length_warabi).items())),np.mean(length_warabi))

print(dict(sorted(Counter(length_sender1_strict).items())),np.mean(length_sender1_strict))

print(dict(sorted(Counter(length_warabi_strict).items())),np.mean(length_warabi_strict))

print(sender1_number_of_message, Warabi_number_of_message)

"""
if __name__ == '__main__':
	sender1_messages=LINE_talk.sender_messages(sender=sender1)

