
import types
from datetime import datetime
from functools import wraps, singledispatch
from numbers import Number, Integral
import typing
import random
from decimal import Decimal
from html import escape

#Monkey patching for annotations
escape.__annotations__ = {1:True}
singledispatch.__annotations__ = {1:True}
wraps.__annotations__ = {1:True}

def is_odd(x:int)->bool:
    "Return true for odd number" 
    return x % 2 != 0


def exec_odd(fn: typing.Callable) -> typing.Callable:
    """Decorator to run given given func only on odd seconds

    Args:
        fn (function): any callable func
    """

    def inner(*args, **kwargs) -> tuple:
        "Executes inner function"
        time = datetime.now()
        print(f'time is {time}')
        if is_odd(time.second):
            return fn(*args, **kwargs)

    return inner


@exec_odd
def add(*args: typing.Tuple) -> Number:
    """ Add n numbers """
    return sum(args)


def logg(fn: typing.Callable) -> typing.Callable:
    """ Add logging functionality to any function """
    from datetime import datetime
    from functools import wraps
    from time import perf_counter

    @wraps(fn)
    def inner(*args, **kwargs):
        run_dt = datetime.utcnow()
        start = perf_counter()
        result = fn(*args, **kwargs)
        time_taken = round(perf_counter() - start, 10)
        print(
            f'{fn.__name__} called at {run_dt} and completed in {time_taken} s with id {hex(id(fn))}')
        print(f'Docsting: \n {fn.__doc__}')
        return result
    return inner


@logg
def mul(a: Number, b: Number) -> Number:
    """ Multiplies two integers"""
    return a*b


def authenticate(fn: typing.Callable) -> typing.Callable:
    """ Authentication decorator for any function """
    username = ''
    password = ''

    def get_username():
        return input('Enter Username')

    def get_password():
        return input('Enter Password')

    def init_user():
        nonlocal username
        nonlocal password
        if not username:
            print('Hi there, Make a new username and password')
            username = get_username()
            password = get_password()

    def inner(*args, **kwargs) -> tuple:
        "Executes inner function"
        init_user()
        if get_username() == username and get_password() == password:
            return fn(*args, **kwargs)

        else:
            return 'You Fraud....'

    return inner


@authenticate
def div(a: Number, b: Number) -> Number:
    """ Divides first number by the second """
    return a/b


def timed(num_times: int) -> typing.Callable:
    "Returns a decorator that can be used to find avg. time for function call"
    def timed_wrapper(fn):
        from time import perf_counter

        @wraps(fn)
        def inner(*args, **kwargs) -> tuple:
            "Executes inner function"
            total_elapsed = 0

            for i in range(num_times):
                start = perf_counter()
                result = fn(*args, **kwargs)
                total_elapsed += perf_counter() - start

            avg_time = total_elapsed / num_times
            print(
                f'{fn.__name__}, Avg Run time: {round(avg_time, 10)} with {num_times} repititions')
            return result
        return inner
    return timed_wrapper


@timed(10)
def sum_n_num(n: int) -> Number:
    "Returns sum of first n natural numbers"
    return n*(n-1)/2


def privilege(prev_level: int = 4) -> typing.Callable:
    """Gives num outputs based on user previleges for a function which returns atleast 4 outputs.

    Args:
        prev_level (int): 1 to 4, with 1 having all access

    Returns:
        typing.Callable: decorator to be used later
    """
    if prev_level not in set([1, 2, 3, 4]):
        raise ValueError('Previlege has to be from 1 to 4.')

    def privilege_wrapper(fn):

        @wraps(fn)
        def inner(*args, **kwargs):

            out = fn(*args, **kwargs)
            if len(out) < 4:
                raise ValueError('Function must return atleast 4 outputs')
            elif prev_level == 1:
                return out
            elif prev_level == 2:
                return out[:-1]
            elif prev_level == 3:
                return out[:-2]
            else:
                return out[:-3]

        return inner
    return privilege_wrapper


@privilege(1)
def return_random_numbers() -> list:
    "Return 4 random numbers"
    return random.choices(range(1000), k=4)


@singledispatch
def htmlize(a: str) -> str:
    "Escape special characters in text"
    return escape(str(a))


@htmlize.register(int)
def html_real(a: int) -> str:
    "return string of given integer"
    return f'{a}'


@htmlize.register(Decimal)
@htmlize.register(float)
def html_real(a: typing.Union[float, Decimal]) -> str:
    "Rounds to two places using bankers rounding off"
    return f'{round(a, 2)}'


@htmlize.register(str)
def html_str(s: str) -> str:
    "Adds a break tag to a new line "
    return html_escape(s).replace('\n', '<br/>\n')


@htmlize.register(tuple)
@htmlize.register(list)
def html_sequence(l: typing.Union[tuple, list]) -> str:
    "Changes tuples and lists to unordered lists"
    items = (f'<li>{html_escape(item)}</li>' for item in l)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


@htmlize.register(dict)
def html_dict(d: dict) -> str:
    "Converts dictionary into key value pairs of unordered lists"
    items = (f'<li>{k}={v}</li>' for k, v in d.items())
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'


@htmlize.register(Integral)
def htmlize_integral_numbers(a: Integral) -> str:
    "For python 2 Integrals are convertes into integers"
    return f'{a}(<i>{str(hex(a))}</i>)'
