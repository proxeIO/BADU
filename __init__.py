'''
Copyright (C) 2023 proxe All Rights Reserved

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    'name': 'Addon Dev Utils',
    'description': 'Blender addon development utils',
    'author': 'proxe',
    'version': (0, 1, '0'),
    'blender': (2, 93),
    'location': 'System Console',
    'category': 'Development'}

from . import addon


def enable_live_reload():
    import bpy

    if not bpy.context:
        return 1.0

    print(F'{bl_info["name"]}: Enabling Live Reload')
    bpy.ops.preferences.addon_enable(module='Live Reload')

    return


def register():
    import bpy
    from os import path, symlink

    print(F'{bl_info["name"]}: Checking for Live Reload')
    scripts = path.join(bpy.utils.user_resource('SCRIPTS'), 'addons')

    # Live reload as a separate addon to accommodate editing this addon without breaking live reload
    if not path.exists(path.join(scripts, 'Live Reload.py')):
        print(F'{bl_info["name"]}: Live reload not found, creating symlink')
        src = path.join(path.dirname(__file__), 'addon', 'reload.py')
        dst = path.join(scripts, 'Live Reload.py')

        symlink(src, dst) # Use symlink so we can keep working from src file (addon/reload.py)

        bpy.app.timers.register(enable_live_reload, first_interval=1.0)

    else:
        print(F'{bl_info["name"]}: Live Reload found')

    addon.register()


def unregister():
    addon.unregister()

