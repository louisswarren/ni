#!/usr/bin/env python3

import ast
import sys

def contains_underscore(expr : ast.Expr, include_stores=False) -> bool:
    match expr:
        case ast.Name(id='_', ctx=ast.Load()):
            return True
        case ast.Name(id='_', ctx=ast.Store()):
            return include_stores
        case ast.Name():
            return False
        case ast.Attribute(value=value):
            return contains_underscore(value)
        case ast.Call(func=func, args=args, keywords=keywords):
            all_arg_values = [func] + args + [kw.value for kw in keywords]
            return any(contains_underscore(arg) for arg in all_arg_values)
        case ast.Lambda(#:
                args=ast.arguments(
                    posonlyargs=posonlyargs,
                    args=args,
                    vararg=vararg,
                    kwonlyargs=kwonlyargs,
                    kwarg=kwarg),
                body=body):
            vararg_l = [vararg] if vararg else []
            kwarg_l = [kwarg] if kwarg else []
            all_args = posonlyargs + args + vararg_l + kwonlyargs + kwarg_l
            if any(arg.arg == '_' for arg in all_args):
                return False
            return contains_underscore(body)
        case ast.GeneratorExp(elt=elt, generators=generators) | \
             ast.ListComp(elt=elt, generators=generators) | \
             ast.SetComp(elt=elt, generators=generators):
            for generator in generators:
                match generator:
                    case ast.comprehension(target=target, iter=it, ifs=ifs):
                        if contains_underscore(it):
                            return True
                        if contains_underscore(target, include_stores=True):
                            return False
                        if any(contains_underscore(x) for x in ifs):
                            return True
                    case _:
                        raise Exception("Unmatched:\n" + ast.dump(expr, indent=4))
            return contains_underscore(elt)
        case ast.DictComp(key=key, value=value, generators=generators):
            for generator in generators:
                match generator:
                    case ast.comprehension(target=target, iter=it, ifs=ifs):
                        if contains_underscore(it):
                            return True
                        if contains_underscore(target, include_stores=True):
                            return False
                        if any(contains_underscore(x) for x in ifs):
                            return True
                    case _:
                        raise Exception("Unmatched:\n" + ast.dump(expr, indent=4))
            return contains_underscore(key) or contains_underscore(value)
        case _:
            children = ast.iter_child_nodes(expr)
            return any(contains_underscore(x) for x in children)
    raise Exception("Unmatched:\n" + ast.dump(expr, indent=4))

def add_underscore(code : str) -> ast.Expr:
    if code[0] == '.':
        code = '_' + code

    expr = ast.parse(code, mode='eval').body

    if contains_underscore(expr):
        return expr

    underscore = ast.Name(id='_', ctx=ast.Load())
    match expr:
        case ast.Call(func=func, args=args, keywords=keywords):
            expr.args = [underscore] + expr.args
            return expr
        case ast.Attribute() | ast.Name():
            return ast.Call(func=expr, args=[underscore], keywords=[])
    raise Exception("Unmatched:\n" + ast.dump(expr, indent=4))

def get_lines():
    while True:
        try:
            yield input()
        except EOFError:
            break

def ni(args, lines):
    output = lines
    for arg in args:
        code = 'lambda _: ' + ast.unparse(add_underscore(arg))
        output = eval(code, {})(output)
    if isinstance(output, str):
        print(output)
    else:
        try:
            it = iter(output)
        except TypeError:
            print(output)
        else:
            for line in it:
                print(line)

if __name__ == '__main__':
    output = get_lines()
    if sys.argv[1:] and sys.argv[1] == '-l':
        for line in output:
            ni(sys.argv[2:], line)
    else:
        ni(sys.argv[1:], get_lines())
