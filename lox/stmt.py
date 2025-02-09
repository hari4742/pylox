from lox.token import Token
from lox.expr import Expr


class Stmt:

    class Visitor:
        def visit_stmt_block(self, stmt: 'Block'):
            pass

        def visit_stmt_expression(self, stmt: 'Expression'):
            pass

        def visit_stmt_if(self, stmt: 'If'):
            pass

        def visit_stmt_print(self, stmt: 'Print'):
            pass

        def visit_stmt_var(self, stmt: 'Var'):
            pass

        def visit_stmt_while(self, stmt: 'While'):
            pass

        def visit_stmt_function(self, stmt: 'Function'):
            pass

        def visit_stmt_return(self, stmt: 'Return'):
            pass

    def accept(self, visitor: Visitor):
        pass


class Block(Stmt):
    statements: list[Stmt]

    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_block(self)


class Expression(Stmt):
    expression: Expr

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_expression(self)


class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_if(self)


class Print(Stmt):
    expression: Expr

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_print(self)


class Var(Stmt):
    name: Token
    initializer: Expr

    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_var(self)


class While(Stmt):
    condition: Expr
    body: Stmt

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_while(self)


class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_function(self)


class Return(Stmt):
    keyword: Token
    value: Expr

    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_return(self)
