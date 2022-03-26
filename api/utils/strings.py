class Strings:
    INTRODUCTION_MESSAGE = \
        "歡迎使用訂票通知系統\n" + \
        "新增訂票任務範例:\n" + \
        "add 身分證, 車種, 起始站, 到達站, 起始時間, 結束時間\n" + \
        "add A121360824, 1, 臺北, 彰化, 2022/03/23-12:00, 2022/03/23-18:00\n" + \
        "車種:1(全部), 2(自強 普悠瑪 太魯閣), 3(莒光)\n" + \
        "query(查詢)\n" + \
        "delete(刪除)"

    COMMAND_DIR = {
        "add": "新增訂票通知",
        "search": ""
    }

    UNKNOWN_COMMAND = "unknown command"

    ADD_BOOKING_TASK_SUCCESS = "新增訂票任務成功"
    QUERY_BOOKING_TASK_RUNNING = "執行中"
    QUERY_BOOKING_TASK_NO_TASK = "沒有任務"
    DELETE_BOOKING_TASK_SUCCESS = "刪除成功"
    ERROR_ALREADY_HAS_TASK = "已經有訂票任務了 一人一張"
    ERROR_ADD_FORMAT = "新增資訊錯誤"
    ERROR_ADD_FORMAT_START_STATION = "沒有此起始站"
    ERROR_ADD_FORMAT_END_STATION = "沒有此到達站"
    ERROR_ADD_FORMAT_Time = "時間輸入錯誤"

    ERROR_QUERY_SEAT = "搜尋車位資訊失敗，請確認格式是正確，或是機器人鼠了"
