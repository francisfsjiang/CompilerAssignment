# encoding: utf-8
import scanner


if __name__ == '__main__':
    s = scanner.Scanner('test_code.ce')
    for i in s.get_token_list():
        print('%10s %10s %10.4f %20s' % (i.token_type, i.lexeme, i.value, i.func))
