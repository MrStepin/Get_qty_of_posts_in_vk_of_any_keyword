import requests
import datetime
import time
import os
import plotly.graph_objects as go
from urllib.error import HTTPError
from dotenv import load_dotenv

VK_API_URL = "https://api.vk.com/method/newsfeed.search/"

def create_dates_list():
    dates_list = [datetime.datetime.now() - datetime.timedelta(days=day) for day in range(1,8)]	
    return dates_list

def create_timestamps_list(dates_list):
    timestamps_list = [time.mktime(datetime_in_list.timetuple()) for datetime_in_list in dates_list]	
    return timestamps_list  

def get_posts_count(list_of_timestamps):
    list_with_count_of_posts_per_day = []
    parameters = PARAMETERS.copy()
    for timestamp in timestamps_list:
        parameters.update({"start_time":timestamp})
        response = requests.get(VK_API_URL, params = parameters)
        response.raise_for_status()
        answer = response.json()
        list_with_count_of_posts_per_day.append(answer["response"]["total_count"])
    return list_with_count_of_posts_per_day

if __name__ == '__main__': 

    load_dotenv()
    secret_key = os.getenv("secret_key")
    PARAMETERS = {
    "q": "Coca-Cola",
    "start_time": "",
    "access_token": secret_key,
    "v": "5.92",
    }
    dates_list = create_dates_list()
    timestamps_list = create_timestamps_list(dates_list)
    posts_count = get_posts_count(timestamps_list)	

    final_graphic = go.Figure(data=go.Bar(y=posts_count, x=dates_list))
    final_graphic.show()

