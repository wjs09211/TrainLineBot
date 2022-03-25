

class UnknownCommandException(Exception):
    """  throw exception when receive unknown command """
    pass


class ParserBookingInfoException(Exception):
    """  throw exception when parser booking ticket information error """
    pass


class ParserBookingInfoStartStationException(Exception):
    pass


class ParserBookingInfoEndStationException(Exception):
    pass


class ParserBookingInfoTimeException(Exception):
    pass


class QueryExistSeatException(Exception):
    pass


class NoMoneyException(Exception):
    pass

