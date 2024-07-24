                    import sys
                    from parser import SappyParser
                    from lexer import SappyLexer

                    class SappyInterpreter:
                        def __init__(self):
                            self.global_scope = {}
                            self.current_scope = self.global_scope

                        def interpret(self, ast):
                            if isinstance(ast, dict):
                                method_name = f"interpret_{ast['type']}"
                                if hasattr(self, method_name):
                                    return getattr(self, method_name)(ast)
                                else:
                                    raise ValueError(f"Unknown AST node type: {ast['type']}")
                            elif isinstance(ast, list):
                                return [self.interpret(node) for node in ast]
                            else:
                                return ast

                        def interpret_Program(self, node):
                            for statement in node['body']:
                                self.interpret(statement)

                        def interpret_Declaration(self, node):
                            value = self.interpret(node['init'])
                            self.current_scope[node['id']] = value

                        def interpret_ExpressionStatement(self, node):
                            return self.interpret(node['expression'])

                        def interpret_BinaryExpression(self, node):
                            left = self.interpret(node['left'])
                            right = self.interpret(node['right'])
                            op = node['operator']
                            if op == '+':
                                return left + right
                            elif op == '-':
                                return left - right
                            elif op == '*':
                                return left * right
                            elif op == '/':
                                return left / right
                            elif op == '%':
                                return left % right
                            elif op == '**':
                                return left ** right
                            elif op == '==':
                                return left == right
                            elif op == '!=':
                                return left != right
                            elif op == '<':
                                return left < right
                            elif op == '>':
                                return left > right
                            elif op == '<=':
                                return left <= right
                            elif op == '>=':
                                return left >= right
                            elif op == '&&':
                                return left and right
                            elif op == '||':
                                return left or right

                        def interpret_UnaryExpression(self, node):
                            argument = self.interpret(node['argument'])
                            op = node['operator']
                            if op == '-':
                                return -argument
                            elif op == '!':
                                return not argument

                        def interpret_Identifier(self, node):
                            return self.current_scope.get(node)

                        def interpret_Literal(self, node):
                            return node['value']

                        def interpret_IfStatement(self, node):
                            test = self.interpret(node['test'])
                            if test:
                                return self.interpret(node['consequent'])
                            elif node['alternate']:
                                return self.interpret(node['alternate'])

                        def interpret_WhileStatement(self, node):
                            while self.interpret(node['test']):
                                self.interpret(node['body'])

                        def interpret_ForStatement(self, node):
                            iterable = self.interpret(node['iterable'])
                            for item in iterable:
                                self.current_scope[node['variable']] = item
                                self.interpret(node['body'])

                        def interpret_FunctionDeclaration(self, node):
                            def func(*args):
                                new_scope = dict(self.current_scope)
                                for param, arg in zip(node['params'], args):
                                    new_scope[param] = arg
                                old_scope = self.current_scope
                                self.current_scope = new_scope
                                result = self.interpret(node['body'])
                                self.current_scope = old_scope
                                return result
                            self.current_scope[node['id']] = func

                        def interpret_ReturnStatement(self, node):
                            return self.interpret(node['argument'])

                        def interpret_CallExpression(self, node):
                            func = self.interpret(node['callee'])
                            args = [self.interpret(arg) for arg in node['arguments']]
                            return func(*args)

                        def interpret_AssignmentExpression(self, node):
                            value = self.interpret(node['right'])
                            self.current_scope[node['left']] = value
                            return value

                        def interpret_Block(self, node):
                            old_scope = self.current_scope
                            self.current_scope = dict(old_scope)
                            for statement in node['body']:
                                self.interpret(statement)
                            self.current_scope = old_scope

                        def interpret_ArrayExpression(self, node):
                            return [self.interpret(element) for element in node['elements']]

                        def interpret_MemberExpression(self, node):
                            obj = self.interpret(node['object'])
                            return getattr(obj, node['property'])

                        def interpret_ImportStatement(self, node):
                            module_name = node['module']
                            if module_name == 'math':
                                import math
                                self.current_scope[module_name] = math
                            else:
                                raise ImportError(f"Cannot import module {module_name}")

                    def run_sappy(code, interpreter):
                        lexer = SappyLexer()
                        parser = SappyParser()

                        try:
                            tokens = lexer.lex(code)
                            ast = parser.parse(tokens)
                            result = interpreter.interpret(ast)
                            return result
                        except Exception as e:
                            print(f"Error: {str(e)}")
                            return None

                    def run_sap_file(filename, interpreter):
                        try:
                            with open(filename, 'r') as file:
                                code = file.read()
                            run_sappy(code, interpreter)
                            print(f"Successfully executed {filename}")
                        except FileNotFoundError:
                            print(f"Error: File '{filename}' not found")
                        except IOError:
                            print(f"Error: Could not read file '{filename}'")
                        except Exception as e:
                            print(f"Error while executing {filename}: {str(e)}")

                    def interactive_mode(interpreter):
                        print("Welcome to the Sappy interactive mode!")
                        print("Type your Sappy code, or 'exit' to quit.")

                        while True:
                            try:
                                user_input = input("sappy> ")
                                if user_input.lower() == 'exit':
                                    break
                                result = run_sappy(user_input, interpreter)
                                if result is not None:
                                    print("Result:", result)
                            except KeyboardInterrupt:
                                print("\nKeyboardInterrupt")
                            except EOFError:
                                break

                        print("Goodbye!")

                    def main():
                        interpreter = SappyInterpreter()

                        if len(sys.argv) == 1:
                            interactive_mode(interpreter)
                        elif len(sys.argv) == 2:
                            filename = sys.argv[1]
                            if not filename.endswith('.sap'):
                                print("Error: File must have a .sap extension")
                            else:
                                run_sap_file(filename, interpreter)
                        else:
                            print("Usage: python main.py [filename.sap]")
                            print("       Run without arguments for interactive mode")

                    if __name__ == "__main__":
                        main()