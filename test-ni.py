import unittest
import ni
import ast

class Test_contains_underscore(unittest.TestCase):
    def get_contains_underscore(self, code):
        return ni.contains_underscore(ast.parse(code, mode='eval').body)

    def assert_contains_underscore(self, code):
        self.assertTrue(self.get_contains_underscore(code))

    def assert_not_contains_underscore(self, code):
        self.assertFalse(self.get_contains_underscore(code))

    def test_basic(self):
        self.assert_contains_underscore('_')

    def test_func(self):
        self.assert_contains_underscore('foo(_)')

    def test_func2(self):
        self.assert_contains_underscore('foo(_, bar)')

    def test_func3(self):
        self.assert_contains_underscore('foo(bar, _)')

    def test_func_is_underscore(self):
        self.assert_contains_underscore('_()')

    def test_func_nested(self):
        self.assert_contains_underscore('foo(bar(_))')

    def test_func_nested2(self):
        self.assert_contains_underscore('foo(baz, bar(_))')

    def test_method(self):
        self.assert_contains_underscore('_.foo()')

    def test_unbound_lambda(self):
        self.assert_contains_underscore('lambda: _')

    def test_unbound_lambda2(self):
        self.assert_contains_underscore('lambda foo: _')

    def test_format(self):
        self.assert_contains_underscore('f"{_}"')

    def test_comprehension(self):
        self.assert_contains_underscore('(a for a in _ for y in b)')
        self.assert_contains_underscore('(a for a in b for y in _)')

    def test_not_basic(self):
        self.assert_not_contains_underscore('foo')

    def test_not_func(self):
        self.assert_not_contains_underscore('foo(_bar, __)')

    def test_not_method_is_underscore(self):
        self.assert_not_contains_underscore('foo._()')

    def test_not_lambda(self):
        self.assert_not_contains_underscore('foo(lambda _: bar)')

    def test_not_lambda2(self):
        self.assert_not_contains_underscore('foo(lambda _: _)')

    def test_not_lambda3(self):
        self.assert_not_contains_underscore('foo(lambda *_: _)')

    def test_not_lambda4(self):
        self.assert_not_contains_underscore('foo(lambda *, _: _)')

    def test_not_lambda5(self):
        self.assert_not_contains_underscore('foo(lambda _=10: _)')

    def test_not_dict_key(self):
        self.assert_not_contains_underscore('{"_": x}')

    def test_not_comprehension(self):
        self.assert_not_contains_underscore('(_ for _ in range(10))')
        self.assert_not_contains_underscore('{_ for _ in range(10)}')
        self.assert_not_contains_underscore('[_ for _ in range(10)]')
        self.assert_not_contains_underscore('{_: _ for _ in range(10)}')
        self.assert_not_contains_underscore('(_ for x in a for _ in b)')
        self.assert_not_contains_underscore('(_ for _ in a for y in b)')

    def test_op_or(self):
        self.assert_contains_underscore('_ or x')

    def test_many_subexpressions(self):
        expr = '_'
        expr = f'x and ({expr})'
        expr = f'x | ({expr})'
        expr = f'not ({expr})'
        expr = f'lambda x: ({expr})'
        expr = f'({expr}) if x else x'
        expr = f'x if ({expr}) else x'
        expr = f'x if x else ({expr})'
        expr = f'{{"x": ({expr})}}'
        expr = f'{{({expr})}}'
        expr = f'[({expr}) for x in y]'
        expr = f'[y for x in ({expr})]'
        expr = f'{{({expr}) for x in y}}'
        expr = f'{{y for x in ({expr})}}'
        expr = f'{{0: ({expr}) for x in y}}'
        expr = f'{{0: y for x in ({expr})}}'
        expr = f'(({expr}) for x in y)'
        expr = f'(y for x in ({expr}))'
        expr = f'(y for x in z if x == ({expr}))'
        expr = f'x < ({expr})'
        expr = f'x[0:-1:({expr})]'
        self.assert_contains_underscore(expr)

class Test_add_underscore(unittest.TestCase):
    def add_underscore(self, code, expected):
        self.assertEqual(ast.unparse(ni.add_underscore(code)), expected)

    def test_no_args(self):
        self.add_underscore('foo()', 'foo(_)')

    def test_args(self):
        self.add_underscore('foo(x, y, z)', 'foo(_, x, y, z)')

    def test_method(self):
        self.add_underscore('bar.foo(x, y, z)', 'bar.foo(_, x, y, z)')

    def test_no_call(self):
        self.add_underscore('foo', 'foo(_)')

    def test_no_call_method(self):
        self.add_underscore('bar.foo', 'bar.foo(_)')

    def test_underscore_method(self):
        self.add_underscore('.foo()', '_.foo()')

    def test_already_underscore_method(self):
        self.add_underscore('_.foo()', '_.foo()')

    def test_explicit_arg(self):
        self.add_underscore('foo(_)', 'foo(_)')

    def test_explicit_arg2(self):
        self.add_underscore('foo(x, _)', 'foo(x, _)')

    def test_explicit_arg_nested(self):
        self.add_underscore('foo(x, bar(y, _))', 'foo(x, bar(y, _))')

    def test_lambda(self):
        self.add_underscore('foo(lambda _: _)', 'foo(_, lambda _: _)')


if __name__ == '__main__':
    unittest.main()
