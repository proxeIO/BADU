import bpy
from os import path, symlink

sep = path.sep
dirname = path.dirname

scripts = join(bpy.utils.user_resource('SCRIPTS'), 'addons')

# validate
del bpy
