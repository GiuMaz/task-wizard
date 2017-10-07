import os

from turingarena.interfaces.codegen.supportgen import AbstractSupportGenerator
from turingarena.interfaces.codegen.utils import indent_all, write_to_file, indent
from turingarena.interfaces.supportgen.cpp.blocks import generate_block
from turingarena.interfaces.supportgen.cpp.declarations import build_declaration, build_parameter
from turingarena.interfaces.supportgen.cpp.types import generate_base_type


class InterfaceItemGenerator:
    def visit_variable_declaration(self, declaration):
        yield build_declaration(declaration)

    def visit_function_declaration(self, decl):
        if hasattr(decl,'return_type'):
            ret_type = generate_base_type(decl.return_type)
        else:
            ret_type = "void"
        yield "{return_type} {name}({arguments});".format(
            return_type=ret_type,
            name=decl.declarator.name,
            arguments=', '.join(build_parameter(p) for p in decl.parameters)
        )

    def visit_callback_declaration(self, decl):
        name = decl.declarator.name
        yield "{return_type} {name}({arguments})".format(
            return_type=
                generate_base_type(decl.return_type)
                if decl.return_type is not None
                else "void",
            name=name,
            arguments=', '.join(build_parameter(p) for p in decl.parameters)
        ) + " {"
        if len(decl.interface.callback_declarations) > 0:
            yield indent(r"""printf("%s\n", "{name}");""".format(name=name))
        yield from indent_all(generate_block(decl.body))
        yield "}"

    def visit_main_declaration(self, declaration):
        yield "int main() {"
        yield from indent_all(generate_block(declaration.body))
        yield "}"


class SupportGenerator(AbstractSupportGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.include_file_path = os.path.join(self.dest_dir, "main.h")
        self.main_file_path = os.path.join(self.dest_dir, "main.cpp")

    def generate(self):
        main_file = open(self.main_file_path, "w")
        write_to_file(self.generate_main_file(), main_file)

    def generate_main_file(self):
        yield "#include <cstdio>"
        yield "#include <cstdlib>"
        generator = InterfaceItemGenerator()
        for item in self.interface.interface_items:
            yield
            yield from item.accept(generator)