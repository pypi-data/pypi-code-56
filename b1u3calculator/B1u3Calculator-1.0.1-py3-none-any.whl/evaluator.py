from b1u3calculator import ast, obj

class EvaluatedError(Exception):
    def __init__(self, msg):
        self.msg = msg


def eval(node, env, funcs):
    if type(node) == ast.IntegerLiteral:
        return obj.Integer(value=node.value)
    elif type(node) == ast.Program:
        res = None
        for s in node.statements:
            res = eval(s, env, funcs)
            if isinstance(res, obj.Return):
                return res
        return res
    elif type(node) == ast.ExpressionStatement:
        return eval(node.expression, env, funcs)
    elif type(node) == ast.PrefixExpression:
        if node.operator == "-":
            right = eval(node.right, env, funcs)
            return obj.Integer(value=-right.value)
        # if add operator, add code here
    elif type(node) == ast.InfixExpression:
        left = eval(node.left, env, funcs)
        right = eval(node.right, env, funcs)
        if node.operator == "+":
            return obj.Integer(value=left.value+right.value)
        elif node.operator == "-":
            return obj.Integer(value=left.value-right.value)
        elif node.operator == "*":
            return obj.Integer(value=left.value*right.value)
        elif node.operator == "/":
            return obj.Integer(value=left.value//right.value)
    elif type(node) == ast.ReturnStatement:
        # If you don't copy value, equate reference value with return value
        integer_obj = eval(node.return_value, env, funcs)
        return obj.Return(value=integer_obj.value)
    elif type(node) == ast.BlockStatement:
        res = obj.Integer(value=0)
        for s in node.statements:
            res = eval(s, env, funcs)
            assert res is not None
            if type(res) == obj.Return:
                return res
        return res
    elif type(node) == ast.AssignStatement:
        val = eval(node.value, env, funcs)
        env[node.name.value] = val
        return env[node.name.value]
    elif type(node) == ast.Identifier:
        try:
            return env[node.value]
        except KeyError:
            raise EvaluatedError(f"identifier not found: {node.value}")
    elif type(node) == ast.FunctionStatement:
        funcs[node.id.value] = {"params": node.parameters, "block": node.block}
        return obj.Integer(value=0)
    elif type(node) == ast.CallExpression:
        try:
            block = funcs[node.function.value]["block"]
            args = funcs[node.function.value]["params"]
            if len(args) != len(node.arguments):
                raise EvaluatedError(f"function {node.function.value} has {len(args)} params, but got {len(node.arguments)} params")
            # 呼ぶ関数に合わせて、呼び出し元から任意のenvをマッピングする
            new_env = {}

            # params is definition
            for p, a in zip(args, node.arguments):
                new_env[p.value] = eval(a, env, funcs)
            return eval(block, new_env, funcs)

        except KeyError:
            raise EvaluatedError(f"function not found: {node.function.value}")

