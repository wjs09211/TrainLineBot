import logging


class TrainLine:
    # 1: '山線', 2: '海線'
    MOUNT = 1
    SEA = 2


TrainLineName = {TrainLine.MOUNT: "山線", TrainLine.SEA: "海線"}


class TrainClass:
    # 1: '普悠瑪', 2: '太魯閣', 3: '自強', 4: '莒光', 5: '復興'
    PUYUMA = 1
    TAROKO = 2
    TZU_CHIANG = 3
    CHU_KUANG = 4
    FU_HSING = 5
    TZU_CHIANG_FAST = 11


TrainClassName = {TrainClass.PUYUMA: "普悠瑪", TrainClass.TAROKO: "太魯閣", TrainClass.TZU_CHIANG: "自強",
                  TrainClass.CHU_KUANG: "莒光", TrainClass.FU_HSING: "復興", TrainClass.TZU_CHIANG_FAST: "自強快"}

TRAIN_CODE_MAP = {
    '1': [TrainClass.PUYUMA, TrainClass.TAROKO, TrainClass.TZU_CHIANG,
          TrainClass.CHU_KUANG, TrainClass.FU_HSING, TrainClass.TZU_CHIANG_FAST],
    '2': [TrainClass.PUYUMA, TrainClass.TAROKO, TrainClass.TZU_CHIANG, TrainClass.TZU_CHIANG_FAST],
    '3': [TrainClass.CHU_KUANG, TrainClass.FU_HSING]
}


class TrainTicket:
    def __init__(self, trn_number, start_time, arrive_time, price, half_price, trn_class_code, train_line,
                 start_station_code, end_station_code, id_card):
        self.trn_number = trn_number
        self.start_time = start_time
        self.arrive_time = arrive_time
        self.price = price
        self.half_price = half_price
        self.trn_class_code = trn_class_code
        self.train_line = train_line
        self.start_station_code = start_station_code
        self.end_station_code = end_station_code
        self.id_card = id_card

        self.ticket_number = None

    def __str__(self):
        if self.ticket_number is not None:
            return "車號: %s\n乘車時間: %s\n到達時間: %s\n價格: %d\n車種: %s %s\n身分證: %s\n訂票代碼: %s"\
                   % (self.trn_number, self.start_time, self.arrive_time, self.price, TrainClassName[self.trn_class_code], TrainLineName[self.train_line], self.id_card, self.ticket_number)
        else:
            return "車號: %s\n乘車時間: %s\n到達時間: %s\n價格: %d\n車種: %s %s" \
                   % (self.trn_number, self.start_time, self.arrive_time, self.price, TrainClassName[self.trn_class_code], TrainLineName[self.train_line])
