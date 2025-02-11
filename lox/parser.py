from lox.token import Token, TokenType
from lox.expr import Expr, Binary, Grouping, Literal, Unary, Variable, Assign, Logical, Call
from lox.stmt import Stmt, Print, Expression, Var, Block, If, While, Function, Return


class ParseError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message


class Parser:
    tokens: list[Token]
    current: int

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements: list[Stmt] = []

        while (not self.is_at_end()):
            statement = self.declaration()
            if statement is not None:
                statements.append(statement)

        return statements

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None

    def function(self, kind: str):
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect {kind} name.")

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after {kind} name.")

        parameters: list[Token] = []

        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(
                TokenType.IDENTIFIER, "Expect parameter name."))

            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    raise self.error(
                        self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(
                    TokenType.IDENTIFIER, "Expect parameter name."))

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before {kind} body.")

        body: list[Stmt] = self.block()

        return Function(name, parameters, body)

    def return_stmt(self):
        keyword: Token = self.previous()

        val: Expr = None

        if not self.check(TokenType.SEMICOLON):
            val = self.expression()

        self.consume(TokenType.SEMICOLON,  "Expect ';' after return value.")

        return Return(keyword, val)

    def var_declaration(self):
        name: Token = self.consume(
            TokenType.IDENTIFIER, "Expect variable name.")

        initializer: Expr = None
        if (self.match(TokenType.EQUAL)):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.RETURN):
            return self.return_stmt()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body: Stmt = self.statement()

        return While(condition, body)

    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Stmt
        if (self.match(TokenType.SEMICOLON)):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition: Expr = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON,  "Expect ';' after loop condition.")

        increment: Expr = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if increment is not None:
            body = Block([
                body,
                Expression(increment)
            ])

        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        if initializer is not None:
            body = Block([
                initializer,
                body
            ])

        return body

    def if_statement(self,) -> Stmt:

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch: Stmt = self.statement()
        else_branch: Stmt = None

        if (self.match(TokenType.ELSE)):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(value)

    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while (not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

        return statements

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr: Expr = self.logical_or()

        if (self.match(TokenType.EQUAL)):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def logical_or(self) -> Expr:
        expr: Expr = self.logical_and()

        while self.match(TokenType.OR):
            operator: Token = self.previous()
            right: Expr = self.logical_and()
            expr = Logical(expr, operator, right)

        return expr

    def logical_and(self) -> Expr:
        expr: Expr = self.equality()

        while self.match(TokenType.AND):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.call()

    def call(self) -> Expr:
        expr: Expr = self.primary()

        while True:
            if (self.match(TokenType.LEFT_PAREN)):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def finish_call(self, callee: Expr):
        arguments: list[Expr] = []

        if (not self.check(TokenType.RIGHT_PAREN)):
            arguments.append(self.expression())

            while self.match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self.error(
                        self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren: Token = self.consume(
            TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types: list[TokenType]):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message):
        from lox.lox import Lox
        Lox.error(token.line, message)
        return ParseError(token, message)

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return
            if self.peek().token_type in [TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]:
                return
            self.advance()
