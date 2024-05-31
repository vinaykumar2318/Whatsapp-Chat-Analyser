import pandas as pd
import re

def dataProcessing(data):
    pattern = '\d{2}/\d{2}/\d{4},\s\d{2}:\d{2}\s-\s'
    msg = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'message':msg, 'dates':dates})
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ')
    users = []
    messages = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['message'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['monthNum'] = df['dates'].dt.month
    df['date'] = df['dates'].dt.day
    df['dayName'] = df['dates'].dt.day_name()
    df['dateFull'] = df['dates'].dt.date
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    period = []
    for hour in df[['dayName','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period'] = period
    df.drop(columns=['dates'], inplace=True)
    return df