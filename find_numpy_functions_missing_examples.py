"""
Find numpy functions whose docstrings do not contain "Examples".
"""

import inspect
import numpy as np


modules = [
    'np',
    'np.char',
    # 'np.compat',
    'np.ctypeslib',
    'np.emath',
    'np.fft',
    'np.lib',
    'np.linalg',
    'np.ma',
    # 'np.math',
    'np.polynomial',
    # 'np.random',
    'np.random.Generator',
    'np.rec',
    # 'np.testing',
]

skip = []

print(f"NumPy version {np.__version__}")
print()

total = 0
all_funcs = []
for module_name in modules:
    mod = eval(module_name)
    objects = [(name, getattr(mod, name))
                   for name in getattr(mod, '__all__', dir(mod))
                       if not name.startswith('_')]
    funcs = [item for item in objects
             if inspect.isroutine(item[1])]
    noex = [item for item in funcs
            if ((module_name + '.' + item[0]) not in skip and
                (item[1].__doc__ is None or
                ("is deprecated" not in item[1].__doc__) and
                ("Examples" not in item[1].__doc__)))]
    noex = [item for item in noex if item not in all_funcs]
    if len(noex) > 0:
        all_funcs.extend(noex)
        noex.sort()
        total += len(noex)
        print(module_name, "(%d)" % len(noex))
        for name, func in noex:
            print("   ", name, end='')
            if func.__doc__ is None:
                print(" \t[no docstring]")
            else:
                print()

print()
print('Found %d functions' % total)
