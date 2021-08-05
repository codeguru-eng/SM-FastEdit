from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES = {
    'tF': format([89, 0, 255]),
    'operator2': format([255, 81, 81], 'bold'),
    'operator3': format([255, 81, 81], 'bold'),
    'operator': format([123, 255, 0], 'italic'),
    'operator4': format('darkgray'),
    'operator5': format([0, 204, 255], 'italic'),
    'operator6': format('red'),
    'brace': format('darkGray'),
    'string': format([255, 230, 0]),
    'this': format([158, 158, 158], 'italic'),
    'funcClass': format([0, 204, 255])
}


class Highlighter(QSyntaxHighlighter):
    """Syntax highlighter for the HTML language.
    """



    operators = [
        ' class=',' id=',' content=',' http-eqiv=',' href=',' src=', ' rel=', ' type=', ' required=', ' placeholder=',' lang=',' style=',
        # on 
        ' onclick=',' onmouseover=',' onmouseout=',
        # other 
        ' draggable=', ' disabled=',' name=', ' target=',' align=',' value=',' required=',' readonly='
    ]
    operators2 = [
        # tags
        '<html ','</html >','<head ','</head >','<body ','</body >','<div ','</div >','<script ','</script >','<title ','</title >','<link ','</link >','<a ','</a >','<h1 ','</h1 >',
        '<h2 ','</h2 >','<h3 ','</h3 >','<h4 ','</h4 >','<h5 ','</h5 >','<h6 ','</h6 >','<p ','</p >','<button ','</button >','<center ','</center >','<form ','</form >','<input ','</input>','<textarea ','</textarea >',
        '<br >','<label ','</label >','<span ','</span >','<ul ','</ul >','<ol ','</ol >','<li ','</li >','<style ','</style >','<img ','</img >','<meta ','</meta >','<table ','</table >',
        '<td ','</td >'
    ]
    operators3 = [
        '<html>','</html>','<head>','</head>','<body>','</body>','<div>','</div>','<script>','</script>','<title>','</title>','<link>','</link>','<a>','</a>','<h1>','</h1>',
        '<h2>','</h2>','<h3>','</h3>','<h4>','</h4>','<h5>','</h5>','<h6>','</h6>','<p>','</p>','<button>','</button>','<center>','</center>','<form>','</form>','<input>','</input>','<textarea>','</textarea>',
        '<br>','<label>','</label>','<span>','</span>','<ul>','</ul>','<ol>','</ol>','<li>','</li>','<style>','</style>','<img>','</img>','<meta>','</meta>','<table>','</table>',
        '<td>','</td >'
    ]
    operators4 = [
        '<!DOCTYPE html ','<!DOCTYPE html>', ' PUBLIC '
    ]
    tFs = [
        'true','false'
    ]
    operators5 = [
        'function ','var '
    ]
    operators6 = [
        '=='
    ]
    thiss = [
        'this'
    ]
    #  braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]','\<','\>','\/','\;','\+','\-','\*','\='
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in Highlighter.operators]
        rules += [(r'%s' % h, 0, STYLES['operator2'])
                  for h in Highlighter.operators2]
        rules += [(r'%s' % i, 0, STYLES['operator3'])
                  for i in Highlighter.operators3]
        rules += [(r'%s' % j, 0, STYLES['operator4'])
                  for j in Highlighter.operators4]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in Highlighter.braces]
        rules += [(r'%s' % c, 0, STYLES['tF'])
                  for c in Highlighter.tFs]
        rules += [(r'%s' % d, 0, STYLES['this'])
                  for d in Highlighter.thiss]
        rules += [(r'%s' % d, 0, STYLES['operator5'])
                  for d in Highlighter.operators5]
        rules += [(r'%s' % e, 0, STYLES['operator6'])
                  for e in Highlighter.operators6]

        # All other rules
        rules += [

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            (r'\bfunction\b\s*(\w+)', 1, STYLES['funcClass'])



        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


   
