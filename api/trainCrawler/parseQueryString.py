from datetime import datetime

# trnClassCodes = [1, 2, 3, 4, 5]  # 123 普悠瑪 太魯閣 自強 # 45莒光復興
train_code_map = {
    '1': [1, 2, 3, 4, 5],
    '2': [1, 2, 3],
    '3': [4, 5]
}

station_code_map = {
    '1': '1000',  # 台北
    '2': '1080',  # 桃園
    '3': '1100',  # 中壢
    '4': '1210',  # 新竹
    '5': '3160',  # 苗栗
    '6': '3300',  # 台中
    '7': '3360',  # 彰化
    '8': '4080',  # 嘉義
    '9': '4220',  # 臺南
    '10': '4400',  # 高雄
    '11': '5000'   # 屏東
}


# customerId, train_code, start_code, end_code, start_time, end_time
def get_query_parm(string):
    # 2020-03-01 08:00:00
    parms = string.strip().replace(' ', '').split(',')
    customer_id = parms[0]
    train_code = train_code_map[parms[1]]
    start_code = station_code_map[parms[2]]
    end_code = station_code_map[parms[3]]
    start_time = datetime.strptime(parms[4], "%Y/%m/%d-%H:%M")
    end_time = datetime.strptime(parms[5], "%Y/%m/%d-%H:%M")
    print(start_code, end_code, start_time, end_time)
    return customer_id, train_code, start_code, end_code, start_time, end_time

if __name__ == "__main__":
    get_query_parm('A148451324, 1, 7, 3, 2020/03/01-08:00, 2020/03/01-15:00')
