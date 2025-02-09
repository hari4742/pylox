import time
from lox.expr import Expr, Literal, Grouping, Unary, Binary, Variable, Assign, Logical, Call
from lox.token import TokenType, Token
from lox.error import LoxRuntimeError
from lox.stmt import Stmt, If, While, Function
from lox.environment import Environment
from lox.lox_callable import LoxCallable
from lox.return_error import ReturnError


class Interpreter(Expr.Visitor, Stmt.Visitor):
    lox_globals = Environment()
    environment = lox_globals

    def __init__(self):
        class Clock(LoxCallable):
            def arity(self):
                return 0

            def call(self, interpreter, arguments):
                return time.time()

            def __str__(self):
                return "<native fn>"

        self.lox_globals.define("clock", Clock())

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            from lox.lox import Lox
            Lox.runtime_error(error)

    def execute(self, statement: Stmt):
        statement.accept(self)

    def visit_stmt_expression(self, stmt):
        self.expression(stmt.expression)
        return None

    def visit_stmt_while(self, stmt: While):

        while (self.is_truthy(self.expression(stmt.condition))):
            self.execute(stmt.body)
        return None

    def visit_stmt_if(self, stmt: If):
        if (self.is_truthy(self.expression(stmt.condition))):
            self.execute(stmt.then_branch)
        elif (stmt.else_branch is not None):
            self.execute(stmt.else_branch)
        return None

    def visit_stmt_print(self, stmt):
        value = self.expression(stmt.expression)
        print(self.stringify(value))
        return None

    def visit_stmt_var(self, stmt):
        value = None

        if (stmt.initializer is not None):
            value = self.expression(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

        return None

    def visit_stmt_function(self, stmt: Function):
        from lox.lox_function import LoxFunction
        function: LoxFunction = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_expr_call(self, expr: Call):
        callee: object = self.expression(expr.callee)
        arguments: list[object] = []

        for argument in expr.arguments:
            arguments.append(self.expression(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(
                expr.paren, "Can only call functions and classes.")

        function: LoxCallable = callee

        if len(arguments) != function.arity():
            raise LoxRuntimeError(
                expr.paren, f"Expected {function.arity()} arguments but got {arguments.size()}.")
        return function.call(self, arguments)

    def visit_stmt_return(self, stmt):
        val: object = None

        if stmt.value is not None:
            val = self.expression(stmt.value)

        raise ReturnError(val)

    def visit_expr_variable(self, expr: Variable):
        return self.environment.get(expr.name)

    def visit_expr_assign(self, expr: Assign):
        value: object = self.expression(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_expr_literal(self, expr: Literal):
        return expr.value

    def visit_expr_logical(self, expr: Logical):
        left: object = self.expression(expr.left)

        if (expr.operator.token_type == TokenType.OR):
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.expression(expr.right)

    def visit_stmt_block(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

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
