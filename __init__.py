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
    'version': (0, 0, '2'),
    'blender': (2, 93),
    'location': 'Text Editor \u2794 Sidebar (CTRL + T) \u2794 Dev \u2794 Addon',
    'category': 'Development'}


def check_live_reload():
    import bpy
    # from os import path, symlink
    from . addon.path import path, symlink

    filename = F'{bl_info["name"]}: Live Reload.py'

    def enable_live_reload(): # Enable live reload addon after startup
        if not bpy.context:
            return 1.0 # Keep timer

        print(F'{bl_info["name"]}: Enabling Live Reload')
        bpy.ops.preferences.addon_enable(module=filename[:-3])
        bpy.ops.wm.save_userpref() # Save preferences to enable live reload on startup

        return # Remove timer


    print(F'{bl_info["name"]}: Checking for Live Reload')
    scripts = path.join(bpy.utils.user_resource('SCRIPTS'), 'addons')

    # Live reload as a separate addon to accommodate editing this addon without breaking live reload
    if not path.exists(path.join(scripts, filename)):
        print(F'{filename} not found, creating symlink')
        src = path.join(path.dirname(__file__), 'addon', 'reload.py')
        dst = path.join(scripts, filename)

        symlink(src, dst) # Use symlink so we can keep working from src file (addon/reload.py)

        bpy.app.timers.register(enable_live_reload, first_interval=1.0)

    else:
        print(F'{bl_info["name"]}: Live Reload found')

check_live_reload() # Check for live reload before registering this addon
del check_live_reload # Removing function from namespace

# Now we can register this addon
from . import addon


def register():
    addon.register()


def unregister():
    addon.unregister()

