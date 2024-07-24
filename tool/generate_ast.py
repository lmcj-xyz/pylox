import sys


class GenerateAst():
    def define_ast(self, output_dir: str, base_name: str, types: list[str]):
        path: str = output_dir + "/" + base_name.lower() + ".py"
        with open(path, "w", encoding="utf-8") as file:
            file.write("from token import Token\n")
            file.write("from abc import ABC, abstractmethod\n")
            file.write("\n\n")
            file.write("class " + base_name + ":\n")
            file.write("    pass\n\n\n")
            self.define_visitor(file, base_name, types)

            for t in types:
                class_name: str = t.split("&")[0].strip()
                fields: str = t.split("&")[1].strip()
                self.define_type(file, base_name, class_name, fields)
                file.write("\n\n")

    def define_visitor(self, file, base_name: str, types: list[str]):
        file.write("class Visitor(ABC):\n")
        for t in types:
            type_name: str = t.split("&")[0].strip()
            file.write("    @abstractmethod\n")
            file.write(
                    "    def visit_" + type_name.lower() + "_"
                    + base_name.lower() + "(" + base_name.lower() + ": "
                    + type_name + "):\n"
                    )
            file.write("        pass\n\n")

    def define_type(self, file, base_name: str, class_name: str, field_list: str):
        file.write("class " + class_name + "(" + base_name + "):\n")
        file.write("    def __init__(self, " + field_list + "):\n")

        fields: str = field_list.split(", ")
        for f in fields:
            name: str = f.split(": ")[0]
            file.write("        self." + name + " = " + name + "\n")

        file.write("\n")
        file.write("    def accept(self, visitor: Visitor):\n")
        file.write(
                "        return visitor.visit_" + class_name
                + "_" + base_name + "(self)\n"
                )


if __name__ == "__main__":
    genast = GenerateAst()
    if len(sys.argv[1:]) != 1:
        sys.stderr.write("Usage: generate_ast <output directory>\n")
        sys.exit(64)
    output_dir = sys.argv[1]

    genast.define_ast(output_dir, "Expr",
                      ["Binary     & left: Expr, operator: Token, right: Expr",
                       "Grouping   & expresion: Expr",
                       "Literal    & value: object",
                       "Unary      & operator: Token, right: Expr"])
