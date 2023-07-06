import requests
from bs4 import BeautifulSoup
import re
import tweepy
from datetime import date

today = date.today()

# 定义用户信息
user_id = '109631939191200721'
# user_id = '110651091149186382'
# user_id ='110651127867774009'
instance_url = "https://mas.to"
# user_token = " xZzrnZLx-6r3sl4dyytrsnV_tA-NpT_kckwTD-FMdgU "
# 文件路径，用于记录已处理的状态
processed_file = "processed_statuses.txt"

date_str = str(today)


#timestamp of a specified date
def get_timestamp(date_str):
    date = datetime.datetime.strptime(data_str,"%Y-%m=%d" )
    timestamp = int(date.timestamp())
    return timestamp

# 获取指定日期以后状态
def get_statuses_after_date(date):
    statuses_url = f"{instance_url}/api/v1/accounts/{user_id}/statuses"
    print("for debug:", statuses_url)
    params = {
        "limit": 100,
        "exclude_replies": True,
        "exclude_reblogs": True
    }
#     headers = {
#         "Authorization": f"Bearer {user_token}"
#     }

    response = requests.get(statuses_url, params=params)

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
        consumer_key="JqpfLSZZGTVj8oUfVqT3vXeV6",
        consumer_secret="fjajSF0CW3BDSgNBeWVfcPcc3AIvuc0zSzcgLW4oHZWLsVmhz5",
        access_token="1520548458645663744-bz1IuNwAQ5Uz2OGLkXrivB0Rq0B2Pb",
        access_token_secret="FDYqoAgnDCkNGIkAD9UZwTNkJyltt5O9CPgPPQYqc9ku6"
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
                
statuses = get_statuses_after_date(date_str)

for status in statuses:
    content = status["content"]
    statusId= status["id"]
    if not is_status_processed(statusId): 
        print("状态内容:", htmlToText(content))
        mark_status_processed(statusId)
        print("---") 