import psycopg2
import psycopg2.extras
import psycopg2.extensions


class Connection:
    conn_string = "host='localhost' dbname='chess' user='www-data' password='NULL'"
    conn = None

    @classmethod
    def connect(cls):
        cls.conn = psycopg2.connect(cls.conn_string)

    @classmethod
    def cursor(cls):
        return cls.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @classmethod
    def execute(cls, query, *params):
        cursor = cls.cursor()
        cursor.execute(query, params)
        return cursor.rowcount, cursor

    @classmethod
    def get_type_oid(cls, name):
        n, curs = cls.execute('select oid from pg_type where typname = %s', name)
        if n==0:
            raise ValueError("could not find type {}".format(name))
        return curs.fetchone()['oid']

    @classmethod
    def register_type(cls, name, func):
        oids = (Connection.get_type_oid(name),) 
        f = psycopg2.extensions.new_type(oids, name, func)
        psycopg2.extensions.register_type(f)
        oids = (Connection.get_type_oid("_"+name),) 
        f = psycopg2.extensions.new_array_type(oids, "_"+name, f)
        psycopg2.extensions.register_type(f)

Connection.connect()

class PieceSquare:
    def __init__(self, val):

        self.piece = chess.Piece.from_symbol(val[0])
        self.square = chess.SQUARE_NAMES.index(val[1:])

    def __str__(self):
        return '{}{}'.format(self.piece, chess.SQUARE_NAMES[self.square])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.piece==other.piece and self.square==other.square

class PieceSquareSubject:

    def __init__(self, val):
        val = list(val)
        self.subject = chess.Piece.from_symbol(val.pop(0))
        self.kind = val.pop(0)
        self.piece = chess.Piece.from_symbol(val.pop(0))
        self.square = chess.SQUARE_NAMES.index(''.join(val))

    def __str__(self):
        return '{}{}{}{}'.format(
                self.subject, self.kind, self.piece, chess.SQUARE_NAMES[self.square])

    def __repr__(self):
        return self.__str__()
    


def db_to_square(val, curs):
    return chess.SQUARE_NAMES.index(val)
Connection.register_type("square", db_to_square)

def db_to_cpiece(val, curs):
    return chess.Piece.from_symbol(val)
Connection.register_type("cpiece", db_to_cpiece)

def db_to_board(val, curs):
    return chess.Board(val + ' 1 1')
Connection.register_type("board", db_to_board)

def db_to_piecesquare(val, curs):
    if val[0] == '+':
        return PieceSquare(val[1:])
    for v in '>/-':
        if v in val:
            return PieceSquareSubject(val)
    return PieceSquare(val)

Connection.register_type("piecesquare", db_to_piecesquare)


class Query(Connection):

    @classmethod
    def random_search(cls):
        c = Connection.cursor()
        n, rows = cls.execute(c, "select * from random_search()")
        for row in rows:
            yield PositionResult(row)

    @classmethod
    def random_position(cls):
        c = Connection.cursor()
        n, rows = cls.execute(c, "select * from v_position order by random() limit 1")
        if n == 0:
            return None
        for row in rows:
            return Position(row)

    @classmethod
    def select_fen(cls, fen):

        c = Connection.cursor()
        n, rows = cls.execute(c, "select * from v_position where fen=%s limit 1", fen)
        if n == 0:
            return None
        return Position(rows.fetchone())


