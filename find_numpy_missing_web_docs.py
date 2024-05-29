#Start by building the docs. 
#Place this file in the .idea/ folder (it's part of numpy's .gitignore). 
#Then run all. 

import os
import types
import inspect
import numpy as np
from sphinx.ext.intersphinx import InventoryFile
from io import BytesIO

current_directory = os.path.os.getcwd()
print("Current Directory:", current_directory)
# Path to the local objects.inv file
obj_file_path = os.path.join(current_directory,'..', 'doc', 'build', 'html', 'objects.inv')

def read_objects_inv(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None

def parse_objects_inv(data):
    # Use InventoryFile to parse the inventory
    inv_file = InventoryFile.load(BytesIO(data), '', lambda uri, rel: rel)
    
    inventory = {}
    for project_name, project_data in inv_file.items():
        inventory[project_name] = {}
        for name, (project, version, uri, display_name) in project_data.items():
            inventory[project_name][name] = (uri, display_name)
    return inventory

def get_inventory_as_text(inventory):
    inventory_text = ""
    for category, items in inventory.items():
        inventory_text += f"\nCategory: {category}\n"
        for name, (location, dispname) in items.items():
            inventory_text += f"  {name} -> {location} ({dispname})\n"
    return inventory_text
    
def get_inventory_text(file_path):
    data = read_objects_inv(file_path)
    if data:
        inventory = parse_objects_inv(data)
        return get_inventory_as_text(inventory)
    else:
        return "Error: Could not read the objects.inv file."

# Get the inventory as text
inventory_text = get_inventory_text(obj_file_path)

modules = [
    #'',
    'exceptions',
    'fft', #Uses automodule
    'linalg',
    'polynomial',
    'random',
    'strings',
    #'testing',
    'typing',
    # Special - Purpose
    'ctypeslib',
    'dtypes',
    'emath',
    'lib',
    'rec',
    'version',
    # legacy
    'char', #Use strings instead
    #'distutils', #deprecated
    'f2py', # legacy
    'ma', # not reliable
    #'matlib', # pending deprecation # Functions are available in main namespace and not documented online. 
]

#Dyanamically get 'numpy._ArrayFunctionDispatcher' as a type to check for.
dispatcher_type = type(getattr(eval('np.linalg'),'matrix_power'))
print(dispatcher_type)

print(f"NumPy version {np.__version__}")
print()

for module_name in modules:
    print('\n',module_name,'\n-----')
    mod = eval('np.' + module_name)
    # This gets the list of public facing items in the module.
    all_items = getattr(mod, '__all__', dir(mod))

    # We want callable functions.
    objects = [(name, getattr(mod, name))
                    for name in getattr(mod, '__all__', dir(mod))
                        if not name.startswith('_')]
    # This returns two items in ma that aren't callable...
    #funcs = [item for item in objects
    #         if inspect.isroutine(item[1])]

    #Using other hack to deal with numpy._ArrayFunctionDispatcher type.
    funcs = [item for item in objects
                if isinstance(item[1], (types.FunctionType,
                                        types.BuiltinFunctionType,
                                        types.MethodDescriptorType,
                                        np.ufunc,
                                        dispatcher_type,
                                        ))]
    
    # Ignore functions that are explicitly deprecated.
    non_deprecated = [item for item in funcs
                      if ("is deprecated" not in item[1].__doc__)]
    # non_deprecated = funcs
    searchfuncs = [item[0] for item in non_deprecated]

    #We can also search through all items, ignoring the type.
    # non_deprecated = all_items
    # searchfuncs = [item for item in non_deprecated]

    missing_rst = [func for func in searchfuncs
                if((module_name + '.' + func + ' ') not in inventory_text )]
    for item in missing_rst: print(item)

