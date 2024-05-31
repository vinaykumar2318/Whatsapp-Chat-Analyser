import pandas as pd
import emoji
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
extract = URLExtract()

def doCalc(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]

    numMsg = df.shape[0]

    words = []
    for msg in df['messages']:
        words.extend(msg.split())

    numMedia = df[df['messages']=="<Media omitted>\n"].shape[0]

    links = []
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))
    
    return numMsg, len(words), numMedia, len(links)

def findActive(df):
    mostActive = df['users'].value_counts().head(6)
    new_df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index':'Name', 'users':'Percent'})
    return mostActive, new_df

def makeWC(userSel,df):
    f = open('hinglish.txt','r')
    stopWords = f.read()

    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    rmvString = '<This message was edited>'
    temp = df[~df['messages'].str.contains(rmvString, case=False, na=False)] 
    temp = temp[temp['users']!="Group Notification"]
    temp = temp[temp['messages']!="<Media omitted>\n"]
    temp = temp[~temp['messages'].str.contains("This message was deleted", case=False, na=False)]
    
    wc = WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    imgWC = wc.generate(temp['messages'].str.cat(sep=" "))
    return imgWC

def mostCWords(userSel,df):
    f = open('hinglish.txt','r')
    stopWords = f.read()

    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    rmvString = '<This message was edited>'
    temp = df[~df['messages'].str.contains(rmvString, case=False, na=False)] 
    temp = temp[temp['users']!="Group Notification"]
    temp = temp[temp['messages']!="<Media omitted>\n"]
    temp = temp[~temp['messages'].str.contains("This message was deleted", case=False, na=False)]

    words = []
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stopWords:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

def mostUEmoji(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if emoji.is_emoji(c)])
    
    emojiDF = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Frequency'])
    return emojiDF


def chatTimeline(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]

    timeline = df.groupby(['year','monthNum','month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def dailyTimeline(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    timelineDaily = df.groupby('dateFull').count()['messages'].reset_index()
    return timelineDaily

def actMapWeek(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    return df['dayName'].value_counts()

def actMapMonth(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    return df['month'].value_counts()

def heatMap(userSel,df):
    if userSel != 'Overall':
        df = df[df['users']==userSel]
    
    return df.pivot_table(index='dayName', columns='period', values='messages', aggfunc='count').fillna(0)