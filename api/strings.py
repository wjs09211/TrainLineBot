class Strings:
    INTRODUCTION_MESSAGE = \
        "歡迎使用訂票通知系統，查詢使用方式輸入help\n" + \
        "(自動訂票開發中...)\n" + \
        "範例:\n" + \
        "add 身分證, 車種, 起始站, 到達站, 起始時間, 到達時間\n" + \
        "add A121360824, 1, 臺北, 彰化, 2022/03/23-12:00, 2022/03/23-18:00\n"

    COMMAND_DIR = {
        "add": "新增訂票通知",
        "search": ""
    }

    UNKNOWN_COMMAND = "unknown command"

    ADD_BOOKING_TASK_SUCCESS = "新增訂票任務成功"
