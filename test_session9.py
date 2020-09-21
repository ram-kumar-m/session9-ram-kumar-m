import session9 as main
import pytest
import random
import os
import inspect
import re
import functools
from datetime import datetime

random_list = random.choices(range(1000), k=5)


main_funcs = [func for func in inspect.getmembers(main) if inspect.isfunction(func[1])]



README_CONTENT_CHECK_FOR = ['exec_odd', 'logg', 'authenticate', 'timed', 'privilege', 'singledispatch', 'htmlize']

CHECK_FOR_THINGS_NOT_ALLOWED = []

def test_for_docstrings():
    for func in main_funcs:
        assert func[1].__doc__ , f'Function {func[0]} has no doc string'

def test_for_annotations():
    for func in main_funcs:
        assert func[1].__annotations__ , f'Function {func[0]} has no annotations'

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"


def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(
        readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"


def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"


def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10


def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(main)
    spaces = re.findall('\n +.', lines)
    for count, space in enumerate(spaces):
        assert len(space) % 4 == 2, f"Your script contains misplaced indentations at \
n'th postion {count+1} starting \n with {space}"
        assert len(re.sub(
            r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"


def test_function_name_had_cap_letter():
    functions = inspect.getmembers(main, inspect.isfunction)
    for function in functions:
        assert len(re.findall(
            '([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_exec_odd():
    time = datetime.now()
    if main.is_odd(time.second):
        assert main.add(1,2) == 3, f'Func works only on odd seconds, {time}'
    else:
        assert main.add(1,2) == None, f'Func works only on odd seconds, {time}'


def test_logg():
    assert main.mul.__doc__, 'Wrapper log func needs a doc string'

def test_mul():
    assert main.mul(random_list[0], random_list[1]) == random_list[0] * random_list[1]  , f'Mul func not working, with not working'    


def test_sum_n_num():
    num = random_list[0]
    assert main.sum_n_num(num) == num*(num-1)/2, 'Check sum_n_num function'

def test_privilege():
    prev_level = random.randint(1,4)
    num_random = 4
    @main.privilege(prev_level)
    def return_random_numbers():
        return random.choices(range(1000), k=num_random)

    out = return_random_numbers()
    assert len(out) == num_random+1-prev_level, 'Lesser the previlege more the output'

def test_privilege_value_error():
    with pytest.raises(ValueError):
        
        prev_level = random.randint(1,4)
        num_random = 3
        @main.privilege(prev_level)
        def return_random_numbers():
            return random.choices(range(1000), k=num_random)

        out = return_random_numbers()

def test_htmlize():
    a = main.htmlize.registry.keys()
    assert len(list(a)) == 9, 'We have given 9 types, hence registry should have 9 elements'
# def test_div():
#     assert main.div(random_list[0], random_list[1]) == random_list[0] / random_list[1]  , f'Div func not working, with not working'