from lox.expr import Expr, Literal, Grouping, Unary, Binary
from lox.token import TokenType, Token
from lox.error import LoxRuntimeError


class Interpreter(Expr.Visitor):

    def interpret(self, expr: Expr):
        try:
            value = self.expression(expr)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            from lox.lox import Lox
            Lox.runtime_error(error)

    def visit_expr_literal(self, expr: Literal):
        return expr.value

    def visit_expr_grouping(self, expr: Grouping):
        return self.expression(expr.expression)

    def visit_expr_unary(self, expr: Unary):
        right = self.expression(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    def visit_expr_binary(self, expr: Binary):
        left = self.expression(expr.left)
        right = self.expression(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(expr.operator,
                                  f"Operands must be two numbers or two strings.")

        elif expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        return None

    def expression(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator: Token, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator,
                              f"Operand must be a number.")

    def check_number_operands(self, operator: Token, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator,
                              f"Operands must be numbers.")

    def stringify(self, value):
        if value is None:
            return "nil"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)
