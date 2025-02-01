from lox.token import Token
from lox.expr import Expr


class Stmt:

    class Visitor:
        def visit_stmt_expression(self, stmt: 'Expression'):
            pass

        def visit_stmt_print(self, stmt: 'Print'):
            pass

        def visit_stmt_var(self, stmt: 'Var'):
            pass

    def accept(self, visitor: Visitor):
        pass


class Expression(Stmt):
    expression: Expr

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_stmt_expression(self)


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
