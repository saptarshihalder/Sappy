from purplex import Lexer, TokenDef

class SappyLexer(Lexer):
    # Whitespace and comments
    WHITESPACE = TokenDef(r'\s+', ignore=True)
    COMMENT = TokenDef(r'#.*', ignore=True)

    # Keywords
    LET = TokenDef(r'let\b')
    CONST = TokenDef(r'const\b')
    FN = TokenDef(r'fn\b')
    RETURN = TokenDef(r'return\b')
    IF = TokenDef(r'if\b')
    ELSE = TokenDef(r'else\b')
    WHILE = TokenDef(r'while\b')
    FOR = TokenDef(r'for\b')
    IN = TokenDef(r'in\b')
    BREAK = TokenDef(r'break\b')
    CONTINUE = TokenDef(r'continue\b')
    IMPORT = TokenDef(r'import\b')
    AS = TokenDef(r'as\b')

    # Literals
    INTEGER = TokenDef(r'\d+')
    FLOAT = TokenDef(r'\d+\.\d+')
    STRING = TokenDef(r'"[^"]*"')
    BOOL = TokenDef(r'true|false')

    # Operators
    PLUS = TokenDef(r'\+')
    MINUS = TokenDef(r'-')
    TIMES = TokenDef(r'\*')
    DIVIDE = TokenDef(r'/')
    MODULO = TokenDef(r'%')
    POWER = TokenDef(r'\*\*')
    EQUALS = TokenDef(r'==')
    NOT_EQUALS = TokenDef(r'!=')
    LESS_THAN = TokenDef(r'<')
    GREATER_THAN = TokenDef(r'>')
    LESS_EQUAL = TokenDef(r'<=')
    GREATER_EQUAL = TokenDef(r'>=')
    AND = TokenDef(r'&&')
    OR = TokenDef(r'\|\|')
    NOT = TokenDef(r'!')

    # Assignment
    ASSIGN = TokenDef(r'=')
    PLUS_ASSIGN = TokenDef(r'\+=')
    MINUS_ASSIGN = TokenDef(r'-=')
    TIMES_ASSIGN = TokenDef(r'\*=')
    DIVIDE_ASSIGN = TokenDef(r'/=')

    # Delimiters
    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')
    LBRACE = TokenDef(r'\{')
    RBRACE = TokenDef(r'\}')
    LBRACKET = TokenDef(r'\[')
    RBRACKET = TokenDef(r'\]')
    COMMA = TokenDef(r',')
    DOT = TokenDef(r'\.')
    COLON = TokenDef(r':')
    SEMICOLON = TokenDef(r';')

    # Identifiers (must come after keywords)
    IDENTIFIER = TokenDef(r'[a-zA-Z_][a-zA-Z0-9_]*')

    def __init__(self, input_text):
        self.input = input_text
        self.tokens = []
        self.position = 0

    def lex(self):
        while self.position < len(self.input):
            matched = False
            for attr_name, attr_value in self.__class__.__dict__.items():
                if isinstance(attr_value, TokenDef):
                    match = attr_value.regexp.match(self.input, self.position)
                    if match:
                        value = match.group(0)
                        if not attr_value.ignore:
                            self.tokens.append((attr_name, value))
                        self.position = match.end()
                        matched = True
                        break
            if not matched:
                raise ValueError(f"Unexpected character at position {self.position}")
        return self.tokens