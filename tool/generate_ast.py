

class GenerateAst:
    @staticmethod
    def main(args: list):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>")
            exit(1)
        output_dir = args[0]
        # GenerateAst.define_ast(output_dir, "Stmt", [
        #     "Expression : Expr expression",
        #     "Print : Expr expression",
        #     "Var : Token name, Expr initializer"
        # ])
        GenerateAst.define_ast(output_dir, "Expr", [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : object value",
            "Unary    : Token operator, Expr right",
            "Variable : Token name"
        ])

    @staticmethod
    def define_ast(output_dir: str, base_name: str, types: list):
        path = output_dir + "/" + base_name.lower() + ".py"
        with open(path, "w") as file:
            file.write("from lox.token import Token\n\n")
            file.write(f"class {base_name}:\n")
            GenerateAst.define_visitor(file, base_name, types)
            GenerateAst.define_accept(file, base_name, types)
            for type in types:
                class_name = type.split(":")[0].strip()
                fields = type.split(":")[1].strip()
                GenerateAst.define_type(file, base_name, class_name, fields)

    @staticmethod
    def define_visitor(file, base_name: str, types: list):
        file.write("\n    class Visitor:\n")
        for type in types:
            type_name = type.split(":")[0].strip()
            file.write(
                f"        def visit_{base_name.lower()}_{type_name.lower()}(self, {base_name.lower()}: '{type_name}'):\n")
            file.write("            pass\n")
        file.write("\n")

    @staticmethod
    def define_accept(file, base_name: str, types: list):
        file.write("\n    def accept(self, visitor: Visitor ):\n")
        file.write("        pass\n\n")

    @staticmethod
    def define_type(file, base_name: str, class_name: str, fields: str):
        file.write(f"\n\nclass {class_name}({base_name}):\n")
        fields = fields.split(", ")
        for field in fields:
            field_name = field.split(" ")[1]
            file.write(f"    {field_name}: {field.split(' ')[0]}\n")
        GenerateAst.define_init(file, class_name, fields)
        GenerateAst.define_type_accept(file, base_name, class_name)

    @staticmethod
    def define_init(file, class_name: str, fields: list):
        file.write(
            f"\n    def __init__(self, {', '.join([field.split(' ')[1] for field in fields])}):\n")
        for field in fields:
            field_name = field.split(" ")[1]
            file.write(f"        self.{field_name} = {field_name}\n")
        file.write("\n")

    @staticmethod
    def define_type_accept(file, base_name: str, class_name: str):
        file.write(f"\n    def accept(self, visitor: Expr.Visitor):\n")
        file.write(
            f"        return visitor.visit_{base_name.lower()}_{class_name.lower()}(self)\n")


if __name__ == "__main__":
    import sys
    GenerateAst.main(sys.argv[1:])
