import requests
from bs4 import BeautifulSoup
import tweepy
from datetime import date
import os
import datetime
import base64

today = date.today()

# define user's info 
user_id = os.environ.get('USER_ID')
instance_url = os.environ.get('INSTANCE_URL')

instance_encoded = os.environ.get('INSTANCE_URL')
print("The content is", instance_encoded)
# file path to record processed statuses
processed_file = "processed_statuses.txt"

date_str = str(today)


#timestamp of a specified date
def get_timestamp(date_str):
    date = datetime.datetime.strptime(date_str,"%Y-%m=%d" )
    timestamp = int(date.timestamp())
    return timestamp

# 获取指定日期以后状态
def get_statuses_after_date(date):
    statuses_url = f"{instance_url}/api/v1/accounts/{user_id}/statuses"
    print("for debug:", statuses_url)
    params = {
        "limit": 10,
        "exclude_replies": True,
        "exclude_reblogs": True
    } 
#     headers = {
#         "Authorization": f"Bearer {user_token}"
#     }

    print("获取状态...")
    response = requests.get(statuses_url, params=params)

    print("状态获取成功")
    if response.status_code == 200:
        statuses = response.json()
        filtered_statuses = [status for status in statuses if status["created_at"]> date]
        return filtered_statuses
    else:
        print("status code: ",response.status_code)
        raise Exception("获取状态失败")

def htmlToText(status_html):

    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(status_html, 'html.parser')

    # 替换链接元素为纯文本形式
    for link in soup.find_all('a'):
#         print(link['href'])
        link.replace_with(link.get_text()+' '+link['href'])

    # 提取纯文本内容
    status_text = soup.get_text()
    return status_text

def tweet(content): 

    client = tweepy.Client(
        consumer_key=os.environ['CONSUMER_KEY'],
        consumer_secret=os.environ['CONSUMER_SECRET'],
        access_token=os.environ.get('ACCESS_TOKEN'),
        access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')
    )

    # send tweet 
    client.create_tweet(text=content)


def latest_status_id(status):
    pass
# 打印状态的内容

# 检查状态是否已处理
def is_status_processed(status_id):
    try:
        with open(processed_file, "r") as file:
            processed_statuses = file.read().splitlines()
            if str(status_id) in processed_statuses: # 已被处理
                return True
            else:
                return False
    except:
        with open(processed_file,'w') as f:
            f.write('')

# 标记状态为已处理
def mark_status_processed(status_id):
    with open(processed_file, "a") as file:
        file.write(str(status_id) + "\n")
    

# debug file
def FileDebug():
    with open(processed_file,'r') as f:
        text = f.read()
        print(text)

      
def FileErase():
     with open(processed_file,'w') as f:
        f.write('')

print('today is', date_str)   
statuses = get_statuses_after_date(date_str)

for status in statuses:
    content = status["content"]
    statusId= status["id"]
    if not is_status_processed(statusId): 
        tweet(htmlToText(content))
        print("状态内容:", htmlToText(content))
        mark_status_processed(statusId)
        print("---") 