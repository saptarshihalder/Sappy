from lexer import SappyLexer
from purplex import Parser, attach, LEFT, RIGHT

class SappyParser(Parser):
    LEXER = SappyLexer
    START = 'program'

    PRECEDENCE = (
        ('right', 'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUALS', 'NOT_EQUALS'),
        ('left', 'LESS_THAN', 'LESS_EQUAL', 'GREATER_THAN', 'GREATER_EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO'),
        ('right', 'POWER'),
        ('right', 'NOT'),
        ('left', 'DOT'),
    )

    @attach('program : statement_list')
    def program(self, statements):
        return {'type': 'Program', 'body': statements}

    @attach('statement_list : statement')
    @attach('statement_list : statement_list statement')
    def statement_list(self, *statements):
        return list(statements)

    @attach('statement : expression_statement')
    @attach('statement : declaration')
    @attach('statement : if_statement')
    @attach('statement : while_statement')
    @attach('statement : for_statement')
    @attach('statement : function_declaration')
    @attach('statement : return_statement')
    @attach('statement : import_statement')
    def statement(self, stmt):
        return stmt

    @attach('expression_statement : expression SEMICOLON')
    def expression_statement(self, expr, _):
        return {'type': 'ExpressionStatement', 'expression': expr}

    @attach('declaration : LET IDENTIFIER ASSIGN expression SEMICOLON')
    @attach('declaration : CONST IDENTIFIER ASSIGN expression SEMICOLON')
    def declaration(self, keyword, identifier, _, value, __):
        return {'type': 'Declaration', 'kind': keyword, 'id': identifier, 'init': value}

    @attach('if_statement : IF LPAREN expression RPAREN block')
    @attach('if_statement : IF LPAREN expression RPAREN block ELSE block')
    def if_statement(self, _, __, condition, ___, consequent, *rest):
        if len(rest) == 2:
            return {'type': 'IfStatement', 'test': condition, 'consequent': consequent, 'alternate': rest[1]}
        return {'type': 'IfStatement', 'test': condition, 'consequent': consequent, 'alternate': None}

    @attach('while_statement : WHILE LPAREN expression RPAREN block')
    def while_statement(self, _, __, test, ___, body):
        return {'type': 'WhileStatement', 'test': test, 'body': body}

    @attach('for_statement : FOR LPAREN IDENTIFIER IN expression RPAREN block')
    def for_statement(self, _, __, variable, ___, iterable, ____, body):
        return {'type': 'ForStatement', 'variable': variable, 'iterable': iterable, 'body': body}

    @attach('function_declaration : FN IDENTIFIER LPAREN parameter_list RPAREN block')
    def function_declaration(self, _, name, __, params, ___, body):
        return {'type': 'FunctionDeclaration', 'id': name, 'params': params, 'body': body}

    @attach('parameter_list : ')
    @attach('parameter_list : IDENTIFIER')
    @attach('parameter_list : parameter_list COMMA IDENTIFIER')
    def parameter_list(self, *params):
        return list(filter(lambda x: x != ',', params))

    @attach('return_statement : RETURN expression SEMICOLON')
    def return_statement(self, _, value, __):
        return {'type': 'ReturnStatement', 'argument': value}

    @attach('import_statement : IMPORT IDENTIFIER SEMICOLON')
    @attach('import_statement : IMPORT IDENTIFIER AS IDENTIFIER SEMICOLON')
    def import_statement(self, _, module, *rest):
        if len(rest) == 3:
            return {'type': 'ImportStatement', 'module': module, 'as': rest[1]}
        return {'type': 'ImportStatement', 'module': module}

    @attach('block : LBRACE statement_list RBRACE')
    @attach('block : LBRACE RBRACE')
    def block(self, _, statements, __):
        return {'type': 'Block', 'body': statements or []}

    @attach('expression : IDENTIFIER')
    @attach('expression : literal')
    @attach('expression : binary_expression')
    @attach('expression : unary_expression')
    @attach('expression : assignment_expression')
    @attach('expression : call_expression')
    @attach('expression : member_expression')
    @attach('expression : array_expression')
    @attach('expression : LPAREN expression RPAREN')
    def expression(self, *args):
        if len(args) == 3:
            return args[1]
        return args[0]

    @attach('literal : INTEGER')
    @attach('literal : FLOAT')
    @attach('literal : STRING')
    @attach('literal : BOOL')
    def literal(self, value):
        return {'type': 'Literal', 'value': value}

    @attach('binary_expression : expression PLUS expression')
    @attach('binary_expression : expression MINUS expression')
    @attach('binary_expression : expression TIMES expression')
    @attach('binary_expression : expression DIVIDE expression')
    @attach('binary_expression : expression MODULO expression')
    @attach('binary_expression : expression POWER expression')
    @attach('binary_expression : expression EQUALS expression')
    @attach('binary_expression : expression NOT_EQUALS expression')
    @attach('binary_expression : expression LESS_THAN expression')
    @attach('binary_expression : expression GREATER_THAN expression')
    @attach('binary_expression : expression LESS_EQUAL expression')
    @attach('binary_expression : expression GREATER_EQUAL expression')
    @attach('binary_expression : expression AND expression')
    @attach('binary_expression : expression OR expression')
    def binary_expression(self, left, operator, right):
        return {'type': 'BinaryExpression', 'operator': operator, 'left': left, 'right': right}

    @attach('unary_expression : MINUS expression', prec_symbol='UMINUS')
    @attach('unary_expression : NOT expression')
    def unary_expression(self, operator, argument):
        return {'type': 'UnaryExpression', 'operator': operator, 'argument': argument}

    @attach('assignment_expression : IDENTIFIER ASSIGN expression')
    @attach('assignment_expression : IDENTIFIER PLUS_ASSIGN expression')
    @attach('assignment_expression : IDENTIFIER MINUS_ASSIGN expression')
    @attach('assignment_expression : IDENTIFIER TIMES_ASSIGN expression')
    @attach('assignment_expression : IDENTIFIER DIVIDE_ASSIGN expression')
    def assignment_expression(self, left, operator, right):
        return {'type': 'AssignmentExpression', 'operator': operator, 'left': left, 'right': right}

    @attach('call_expression : expression LPAREN argument_list RPAREN')
    def call_expression(self, callee, _, args, __):
        return {'type': 'CallExpression', 'callee': callee, 'arguments': args}

    @attach('argument_list : ')
    @attach('argument_list : expression')
    @attach('argument_list : argument_list COMMA expression')
    def argument_list(self, *args):
        return list(filter(lambda x: x != ',', args))

    @attach('member_expression : expression DOT IDENTIFIER')
    def member_expression(self, object, _, property):
        return {'type': 'MemberExpression', 'object': object, 'property': property}

    @attach('array_expression : LBRACKET argument_list RBRACKET')
    def array_expression(self, _, elements, __):
        return {'type': 'ArrayExpression', 'elements': elements}