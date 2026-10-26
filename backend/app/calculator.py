import ast
import operator


class CalculationError(Exception):
    pass


_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class Calculator:
    def evaluate(self, expression: str) -> float:
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            raise CalculationError(f"Invalid expression: {expression!r}")
        return self._eval_node(tree.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in _ALLOWED_BINOPS:
                raise CalculationError(f"Operator not allowed: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            try:
                return _ALLOWED_BINOPS[op_type](left, right)
            except ZeroDivisionError:
                raise CalculationError("Division by zero")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in _ALLOWED_UNARYOPS:
                raise CalculationError(f"Operator not allowed: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return _ALLOWED_UNARYOPS[op_type](operand)

        raise CalculationError(f"Disallowed expression element: {type(node).__name__}")
