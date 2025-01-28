from lox.expr import Binary, Grouping, Literal, Unary, Expr


class AstPrinter(Expr.Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_expr_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_expr_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_expr_literal(self, expr: Literal):
        if expr.value is None:
            return "nil"
        if expr.value is True:
            return "true"
        if expr.value is False:
            return "false"
        return str(expr.value)

    def visit_expr_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs: list[Expr]):
        result = "(" + name
        for expr in exprs:
            result += " "
            result += expr.accept(self)
        result += ")"
        return result
