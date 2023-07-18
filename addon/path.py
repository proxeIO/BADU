import bpy
from os import path, symlink

sep = path.sep
abspath = path.abspath
dirname = path.dirname
basename = path.basename
exists = path.exists
join = path.join

scripts = join(bpy.utils.user_resource('SCRIPTS'), 'addons')

# validate
del bpy
