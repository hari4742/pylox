from lox.token import Token


class Expr:

    class Visitor:
        def visit_expr_assign(self, expr: 'Assign'):
            pass

        def visit_expr_binary(self, expr: 'Binary'):
            pass

        def visit_expr_grouping(self, expr: 'Grouping'):
            pass

        def visit_expr_literal(self, expr: 'Literal'):
            pass

        def visit_expr_logical(self, expr: 'Logical'):
            pass

        def visit_expr_unary(self, expr: 'Unary'):
            pass

        def visit_expr_variable(self, expr: 'Variable'):
            pass

    def accept(self, visitor: Visitor):
        pass


class Assign(Expr):
    name: Token
    value: Expr

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_assign(self)


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

    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_literal(self)


class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_logical(self)


class Unary(Expr):
    operator: Token
    right: Expr

    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_unary(self)


class Variable(Expr):
    name: Token

    def __init__(self, name):
        self.name = name

    def accept(self, visitor: Expr.Visitor):
        return visitor.visit_expr_variable(self)
