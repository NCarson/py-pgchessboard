import types
import time
import sys

#package
import psycopg2
import psycopg2.extras
import psycopg2.extensions

import chess

#local
from svgboard import SvgBoard
from newsvg import ChessBoardSvg

def timit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        sys.stderr.write('func:%r args:[%r, %r] took: %2.4f sec\n' % \
          (f.__name__, args, kw, te-ts))
        return result
    return timed

class Connection:
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'"
    conn = None

    @classmethod
    def register_alchemy(cls, engine, user, dbname, host='localhost', password='NULL'):
        cls.conn = engine.raw_connection().connection
        cls._register_adapters()

    @classmethod
    def register_orm(cls, conn):
        cls.conn = conn
        cls._register_adapters()

    @classmethod
    def commit(cls):
        cls.conn.commit()

    @classmethod
    def connect(cls, user, dbname,
            host='localhost', password=None,
            disable_adapters=False, conn=None):
        if not conn:
            s = cls.conn_string.format(host, dbname, user, password)
            if password:
                s + " password='{}'".format(password)
            cls.conn = psycopg2.connect(s)
        else:
            cls.conn = conn

        if not disable_adapters:
            cls._register_adapters()

    @classmethod
    def _register_adapters(cls):
        cls.register_type("square", db_to_square)
        cls.register_type("cpiece", db_to_cpiece)
        cls.register_type("board", db_to_board)
        cls.register_type("piecesquare", db_to_piecesquare)
        cls.register_type("rank", db_to_rank)
        cls.register_type("cfile", db_to_cfile)

    @classmethod
    def cursor(cls):
        if cls.conn is None:
            raise ValueError("not connected")
        return cls.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @classmethod
    def execute(cls, query, *params):
        if cls.conn is None:
            raise ValueError("not connected")
        cursor = cls.cursor()
        cursor.execute(query, params)
        return cursor.rowcount, cursor

    @classmethod
    def get_type_oid(cls, name):
        if cls.conn is None:
            raise ValueError("not connected")
        n, curs = cls.execute('select oid from pg_type where typname = %s', name)
        if n==0:
            raise ValueError("could not find type {}".format(name))
        return curs.fetchone()['oid']

    @classmethod
    def register_type(cls, name, func):
        if cls.conn is None:
            raise ValueError("not connected")
        oids = (Connection.get_type_oid(name),) 
        f = psycopg2.extensions.new_type(oids, name, func)
        psycopg2.extensions.register_type(f)
        oids = (Connection.get_type_oid("_"+name),) 
        f = psycopg2.extensions.new_array_type(oids, "_"+name, f)
        psycopg2.extensions.register_type(f)


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
    
def db_to_cfile(val, curs):
    return val

def db_to_rank(val, curs):
    return val

def db_to_square(val, curs):
    return chess.SQUARE_NAMES.index(val)

def db_to_cpiece(val, curs):
    return chess.Piece.from_symbol(val)

def db_to_board(val, curs):

    if not val:
        return
    if len(val.split()) != 6:
        val = val + ' 0 0'
    board = chess.Board(val)
    board.to_svg = types.MethodType(to_svg, board)
    return board

def db_to_piecesquare(val, curs):
    if val[0] == '+':
        return PieceSquare(val[1:])
    for v in '>/-':
        if v in val:
            return PieceSquareSubject(val)
    return PieceSquare(val)


def to_svg(board, size, comp=None, title=None, legend=True, fen=True, labels=False, href=None):
    svg = SvgBoard(size=size, labels=labels)
    for (square, piece) in iter_piecesquares(board):
        svg.add_piece(square, piece)
        if comp and comp.piece_at(square) == piece:
            svg.add_circle(square)

    if comp:
        for (square, piece) in iter_piecesquares(comp):
            if board.piece_at(square) != piece:
                svg.add_circle(square, stroke='red')

    if legend:
        svg.add_legend()
    if fen:
        svg.add_caption("{}".format(board.fen()))
    if title:
        svg.add_title("{}".format(title), href=href)

    return svg.tostring()

def to_svg(board, size, comp=None, title=None, legend=True, fen=True, labels=False, href=None):
    svg = ChessBoardSvg(board, size)
    return svg.to_svg(comp=comp)

def iter_piecesquares(board):
    for i in range(64):
        bb = (56 - (i//8)*8 + (i%8)) #fen order
        p = board.piece_at(bb)
        if p:
            yield bb, p


if __name__ == '__main__':

    Connection.connect('www-data')
    @timeit
    def time_board():
        n, rows = Connection.execute("select 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'::board from generate_series(1,1000)")
        for r in rows:
            (rows.fetchone()[0])

    time_board()

