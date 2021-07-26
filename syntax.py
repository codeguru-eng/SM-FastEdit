# Created by Seounghun, Chung <4uwingnet@naver.com>
# Modified by Shaurya Mishra





from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtWidgets import *
 
def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
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
    'keyword': format('#91ff00'),
    'operator': format('#91ff00'),
    'operato2': format('#41c1fc'),
    'froImp': format('#41c1fc', 'italic'),
    'brace': format('darkGray'),
    'newclass': format('lightBlue'),
    'string': format('#faf890'),
    'string2': format('#faf890'),
    'comment': format('gray', 'italic'),
    'mys': format('orange', 'italic'),
    'brace2': format('#91ff00')
}

class HTMLHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the HTML language.
    """
# Spl keywords
    keywords = [
        'lang'
    ]
    # Spl operators
    operators = [
        'http-equiv'
    ]
    operato2s = [
        'html','head','body','script',

        #closing
        '/html','/head','/body','/script'
    ]
    froImpS = [
        'Int','Str','Decml','Main','Hr',"Min","Sec",
    ]
    # Spl braces
    braces = [
        '\{', '\}', '\[', '\]','\(', '\)',
    ]
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])
 
        rules = []
 
        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in HTMLHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in HTMLHighlighter.operators]
        rules += [(r'%s' % o, 0, STYLES['operato2'])
            for o in HTMLHighlighter.operato2s]
        rules += [(r'\b%s\b' % s, 0, STYLES['froImp'])
            for s in HTMLHighlighter.froImpS]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in HTMLHighlighter.braces]

 
        # All other rules
        rules += [
            # 'self'
            (r'\bmys\b', 0, STYLES['mys']),
 
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
 
            # 'def' followed by an identifier
            (r'\bN\b\s*(\w+)', 1, STYLES['newclass']),
 
            # From '#' until a newline
            (r'-:[^//]*', 0, STYLES['comment']),

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
 
        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)
 
 
    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()
 
        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)
 
        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
