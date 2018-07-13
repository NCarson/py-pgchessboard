
import chess

def to_bb_idx(i):
    #from chess square idx, i.ie 1st quadrant math
    return (56 - (i//8)*8 + (i%8))

class ChessBoardSvg:
    svg = '<svg baseProfile="full" height="{}" version="1.1" viewBox="-5,0,69,76" width="{}" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">'
    header = '''
 <defs><marker id="id2" markerHeight="8" markerWidth="8" orient="auto" refX="2" refY="6.25" viewBox="-5,-5,32,32"><path class="arrowhead" d="M2,1 L2,11 L10,6 L2,1" /></marker>
    </defs>
    <g class="chessboard">
	<rect class="blacksquare" height="8" id="a8" width="8" x="0" y="0" /> <rect class="whitesquare" height="8" id="b8" width="8" x="8" y="0" /> <rect class="blacksquare" height="8" id="c8" width="8" x="16" y="0" /> <rect class="whitesquare" height="8" id="d8" width="8" x="24" y="0" /> <rect class="blacksquare" height="8" id="e8" width="8" x="32" y="0" /> <rect class="whitesquare" height="8" id="f8" width="8" x="40" y="0" /> <rect class="blacksquare" height="8" id="g8" width="8" x="48" y="0" /> <rect class="whitesquare" height="8" id="h8" width="8" x="56" y="0" />
	<rect class="whitesquare" height="8" id="a7" width="8" x="0" y="8" /><rect class="blacksquare" height="8" id="b7" width="8" x="8" y="8" /><rect class="whitesquare" height="8" id="c7" width="8" x="16" y="8" /><rect class="blacksquare" height="8" id="d7" width="8" x="24" y="8" /><rect class="whitesquare" height="8" id="e7" width="8" x="32" y="8" /><rect class="blacksquare" height="8" id="f7" width="8" x="40" y="8" /><rect class="whitesquare" height="8" id="g7" width="8" x="48" y="8" /><rect class="blacksquare" height="8" id="h7" width="8" x="56" y="8" />
	<rect class="blacksquare" height="8" id="a6" width="8" x="0" y="16" /><rect class="whitesquare" height="8" id="b6" width="8" x="8" y="16" /><rect class="blacksquare" height="8" id="c6" width="8" x="16" y="16" /><rect class="whitesquare" height="8" id="d6" width="8" x="24" y="16" /><rect class="blacksquare" height="8" id="e6" width="8" x="32" y="16" /><rect class="whitesquare" height="8" id="f6" width="8" x="40" y="16" /><rect class="blacksquare" height="8" id="g6" width="8" x="48" y="16" /><rect class="whitesquare" height="8" id="h6" width="8" x="56" y="16" />
	<rect class="whitesquare" height="8" id="a5" width="8" x="0" y="24" /><rect class="blacksquare" height="8" id="b5" width="8" x="8" y="24" /><rect class="whitesquare" height="8" id="c5" width="8" x="16" y="24" /><rect class="blacksquare" height="8" id="d5" width="8" x="24" y="24" /><rect class="whitesquare" height="8" id="e5" width="8" x="32" y="24" /><rect class="blacksquare" height="8" id="f5" width="8" x="40" y="24" /><rect class="whitesquare" height="8" id="g5" width="8" x="48" y="24" /><rect class="blacksquare" height="8" id="h5" width="8" x="56" y="24" />
	<rect class="blacksquare" height="8" id="a4" width="8" x="0" y="32" /><rect class="whitesquare" height="8" id="b4" width="8" x="8" y="32" /><rect class="blacksquare" height="8" id="c4" width="8" x="16" y="32" /><rect class="whitesquare" height="8" id="d4" width="8" x="24" y="32" /><rect class="blacksquare" height="8" id="e4" width="8" x="32" y="32" /><rect class="whitesquare" height="8" id="f4" width="8" x="40" y="32" /><rect class="blacksquare" height="8" id="g4" width="8" x="48" y="32" /><rect class="whitesquare" height="8" id="h4" width="8" x="56" y="32" />
	<rect class="whitesquare" height="8" id="a3" width="8" x="0" y="40" /><rect class="blacksquare" height="8" id="b3" width="8" x="8" y="40" /><rect class="whitesquare" height="8" id="c3" width="8" x="16" y="40" /><rect class="blacksquare" height="8" id="d3" width="8" x="24" y="40" /><rect class="whitesquare" height="8" id="e3" width="8" x="32" y="40" /><rect class="blacksquare" height="8" id="f3" width="8" x="40" y="40" /><rect class="whitesquare" height="8" id="g3" width="8" x="48" y="40" /><rect class="blacksquare" height="8" id="h3" width="8" x="56" y="40" />
	<rect class="blacksquare" height="8" id="a2" width="8" x="0" y="48" /><rect class="whitesquare" height="8" id="b2" width="8" x="8" y="48" /><rect class="blacksquare" height="8" id="c2" width="8" x="16" y="48" /><rect class="whitesquare" height="8" id="d2" width="8" x="24" y="48" /><rect class="blacksquare" height="8" id="e2" width="8" x="32" y="48" /><rect class="whitesquare" height="8" id="f2" width="8" x="40" y="48" /><rect class="blacksquare" height="8" id="g2" width="8" x="48" y="48" /><rect class="whitesquare" height="8" id="h2" width="8" x="56" y="48" />
	<rect class="whitesquare" height="8" id="a1" width="8" x="0" y="56" /><rect class="blacksquare" height="8" id="b1" width="8" x="8" y="56" /><rect class="whitesquare" height="8" id="c1" width="8" x="16" y="56" /><rect class="blacksquare" height="8" id="d1" width="8" x="24" y="56" /><rect class="whitesquare" height="8" id="e1" width="8" x="32" y="56" /><rect class="blacksquare" height="8" id="f1" width="8" x="40" y="56" /><rect class="whitesquare" height="8" id="g1" width="8" x="48" y="56" /><rect class="blacksquare" height="8" id="h1" width="8" x="56" y="56" />
    </g>
    <g class="legend">
        <text x="-3" y="5">8</text><text x="-3" y="13">7</text><text x="-3" y="21">6</text><text x="-3" y="29">5</text>
        <text x="-3" y="37">4</text><text x="-3" y="45">3</text><text x="-3" y="53">2</text><text x="-3" y="61">1</text>
        <text x="3" y="66">a</text><text x="11" y="66">b</text><text x="19" y="66">c</text><text x="27" y="66">d</text>
        <text x="35" y="66">e</text><text x="43" y="66">f</text><text x="51" y="66">g</text><text x="59" y="66">h</text>
    </g>
    '''
    piece_svg = '<use transform="translate({},{})" xlink:href="#{}" />'
    caption_svg = '''<g class="caption"><text x="0" y="69">{}</text></g>'''
    circle_svg = '<circle cx="{}" cy="{}" r="{}" stroke="{}" stroke-width="{}" fill="{}"/>'


    piece_names = {
            'P':'white-pawn', 'N':'white-knight', 'B':'white-bishop', 'R':'white-rook', 'Q':'white-queen', 'K':'white-king',
            'p':'black-pawn', 'n':'black-knight', 'b':'black-bishop', 'r':'black-rook', 'q':'black-queen', 'k':'black-king',
    }

    def __init__(self, board, size):
        self.board = board
        self.size = size

    def _square_offset(self, square):
        i = to_bb_idx(square)
        x, y = i%8, i//8
        return x*8, y*8

    def _piece(self, square, piece):
        name = self.piece_names[str(piece)]
        xc, yc = self._square_offset(square)
        x, y = xc*7+4, yc*7+2,
        return self.piece_svg.format(x, y, name)

    def add_circle(self, square, stroke='black'):
        name = '{}-circle'.format(chess.SQUARE_NAMES[square])
        xc, yc = self._square_offset(square)
        return self.circle_svg.format(xc*7+4*7, yc*7+4*7, 3.5*7, stroke, 3, 'none')

    def to_svg(self, comp=None):
        out = self.svg.format(self.size, self.size)
        out += self.header
        out += '<g class="pieces" transform="scale(0.143)">\n'
        for square, piece in self.board.piece_map().items():
            out += self._piece(square, piece) + '\n'
            if comp and comp.piece_at(square) != piece:
                out += self.add_circle(square, 'red')
            if comp and comp.piece_at(square) == piece:
                out += self.add_circle(square, 'blue')

        if comp:
            for square, piece in comp.piece_map().items():
                if self.board.piece_at(square) != piece:
                    out += self.add_circle(square, 'red')

        out += '</g>'
        out += self.caption_svg.format(self.board.fen()) + '\n'
        out += '</svg>'
        return out

        #svg.add_circle(square, stroke='orange')


if __name__ == '__main__':
    import chess
    svg = ChessBoardSvg(chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'), 250)
    print(svg.to_svg())

