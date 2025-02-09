from lox.lox_callable import LoxCallable
from lox.stmt import Function
from lox.environment import Environment
from lox.return_error import ReturnError


class LoxFunction(LoxCallable):

    closuer: Environment

    def __init__(self, declaration: Function, closuer: Environment):
        self.declaration: Function = declaration
        self.closuer = closuer

    def call(self, interpreter, arguments):

        environment: Environment = Environment(self.closuer)

        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnError as return_val:
            return return_val.value

        return None

    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
