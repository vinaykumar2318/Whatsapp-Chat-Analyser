# Chat Analysis Project

This project provides tools to analyze chat data from messaging platforms. It includes functions to calculate various statistics, generate word clouds, find the most common words and emojis, and create various visualizations of chat activity. The analysis results are presented using Streamlit for an interactive web-based interface.
You can access the app here :-  <a href="https://whatsapp-chat-analyser-2318.streamlit.app/" target="_blank">https://whatsapp-chat-analyser-2318.streamlit.app/</a>

## Features

- Calculate basic statistics about messages, words, media, and links.
- Identify the most active users in the chat.
- Generate word clouds based on chat messages.
- Find the most common words and emojis.
- Generate timelines for chat activity.
- Create heatmaps and activity maps.
- Interactive visualization using Streamlit.

## Requirements

- Python 3.x
- pandas
- emoji
- wordcloud
- urlextract
- streamlit
- seaborn

## Installation

1. Clone the repository or download the source code.
2. Install the required packages using pip:

    ```sh
    pip install pandas emoji wordcloud urlextract streamlit seaborn
    ```

3. Ensure you have the `hinglish.txt` file in the project directory. This file should contain stopwords used to filter out common words.

## Usage

1. Run the following command in terminal to access the web app:

    ```sh
    streamlit run app.py
    ```

2. Download a chat.txt file in 24-hour format and now you are ready to do analysis on it.
