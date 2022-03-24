

class UnknownCommandException(Exception):
    """  throw exception when receive unknown command """
    pass


class ParserBookingInfoException(Exception):
    """  throw exception when parser booking ticket information error """
    pass


class QueryExistSeatException(Exception):
    pass