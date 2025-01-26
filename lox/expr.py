from lox.token import Token


class Expr:

    class Visitor:
        def visit_expr_binary(self, expr: 'Binary'):
            pass

        def visit_expr_grouping(self, expr: 'Grouping'):
            pass

        def visit_expr_literal(self, expr: 'Literal'):
            pass

        def visit_expr_unary(self, expr: 'Unary'):
            pass

    def accept(self, visitor: Visitor):
        pass


class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_binary(self)


class Grouping(Expr):
    expression: Expr

    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_grouping(self)


class Literal(Expr):
    value: object

    def __init__(self, value):
        self.value = value

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_literal(self)


class Unary(Expr):
    operator: Token
    right: Expr

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_unary(self)
