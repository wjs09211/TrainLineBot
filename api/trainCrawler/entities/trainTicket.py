import logging


class TrainLine:
    # 1: '山線', 2: '海線'
    MOUNT = 1
    SEA = 2


TrainLineName = {TrainLine.MOUNT: "山線", TrainLine.SEA: "山線"}


class TrainClass:
    # 1: '普悠瑪', 2: '太魯閣', 3: '自強', 4: '莒光', 5: '復興'
    PUYUMA = 1
    TAROKO = 2
    TZU_CHIANG = 3
    CHU_KUANG = 4
    FU_HSING = 5


TrainClassName = {TrainClass.PUYUMA: "普悠瑪", TrainClass.TAROKO: "太魯閣", TrainClass.TZU_CHIANG: "自強",
                  TrainClass.CHU_KUANG: "莒光", TrainClass.FU_HSING: "復興"}

TRAIN_CODE_MAP = {
    '1': [TrainClass.PUYUMA, TrainClass.TAROKO, TrainClass.TZU_CHIANG,
          TrainClass.CHU_KUANG, TrainClass.FU_HSING],
    '2': [TrainClass.PUYUMA, TrainClass.TAROKO, TrainClass.TZU_CHIANG],
    '3': [TrainClass.CHU_KUANG, TrainClass.FU_HSING]
}


class TrainTicket:
    def __init__(self, number, start_time, arrive_time, price, trn_class_code, train_line):
        self.number = number
        self.start_time = start_time
        self.arrive_time = arrive_time
        self.price = price
        self.trn_class_code = trn_class_code
        self.train_line = train_line

    def show_info(self):
        logging.info('#' * 50)
        logging.info('車碼: %s' % self.number)
        logging.info(self.start_time)
        logging.info(self.arrive_time)
        logging.info(self.price)
        logging.info(self.trn_class_code)  # 4莒光 3自強
        logging.info(self.train_line)  # 1山線 2海線
        logging.info('#' * 50)

    def __str__(self):
        return "車號: %s\n乘車時間: %s\n到達時間: %s\n價格: %d\n車種: %s %s" % (self.number, self.start_time, self.arrive_time, self.price, TrainClassName[self.trn_class_code], TrainLineName[self.train_line])
