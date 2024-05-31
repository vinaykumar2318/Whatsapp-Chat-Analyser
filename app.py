import streamlit as st
import dataProcess, functions
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = dataProcess.dataProcessing(data)

    userList = df['users'].unique().tolist()
    userList.remove('Group Notification')
    userList.sort()
    userList.insert(0,'Overall')
    userSel = st.sidebar.selectbox("Show Analysis w.r.t :", userList)

    if st.sidebar.button("Show Analysis"):
        #in this we calculating basic stats for group
        numMsg, numWords, numMedia, numLink = functions.doCalc(userSel,df)
        st.title("About Chat :-")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(numMsg)
        with col2:
            st.header("Total Words")
            st.title(numWords)
        with col3:
            st.header("Total Media Shared")
            st.title(numMedia)
        with col4:
            st.header("Total Links Shared")
            st.title(numLink)

        #timeline for chats
        st.title("Monthly Timeline")
        timeline = functions.chatTimeline(userSel,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #timelineDaily for chats
        st.title("Daily Timeline")
        timelineDaily = functions.dailyTimeline(userSel,df)
        fig,ax = plt.subplots()
        ax.plot(timelineDaily['dateFull'],timelineDaily['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map of group
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busyDay = functions.actMapWeek(userSel,df)
            fig, ax = plt.subplots()
            ax.bar(busyDay.index,busyDay.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busyMonth = functions.actMapMonth(userSel,df)
            fig, ax = plt.subplots()
            ax.bar(busyMonth.index,busyMonth.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heat-map for activity of users
        st.title("Weekly Heat Map of Users")
        heatActivity = functions.heatMap(userSel,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatActivity)
        st.pyplot(fig)

        #finding the most active user
        if userSel=='Overall':
            st.title('Most Active Users')
            mostActive, new_df = functions.findActive(df)
            fig, ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(mostActive.index,mostActive.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #now we will form a wordcloud
        st.title("Wordcloud")
        imgWC = functions.makeWC(userSel,df)
        fig,ax = plt.subplots()
        ax.imshow(imgWC)
        st.pyplot(fig)

        #most recently used words
        mostUsed = functions.mostCWords(userSel,df)
        fig,ax = plt.subplots()
        plt.xticks(rotation='vertical')
        ax.bar(mostUsed['Word'],mostUsed['Frequency'])
        st.title("Most Common Words")
        st.pyplot(fig)

        #emoji's analysis
        st.title("Emojis Used In this Chat")
        emojiDF = functions.mostUEmoji(userSel,df)
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emojiDF)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emojiDF['Frequency'].head(10), labels=emojiDF['Emoji'].head(10), autopct="%0.2f")
            st.pyplot(fig)