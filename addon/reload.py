# Symlinked, registration failures here will result in loss of live reload functionality.
# This will require manually enabling the live reload addon in preferences once correct.
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
    'name': 'Addon Dev Utils: Live Reload',
    'description': 'Live reload enabled addons when a source change is detected.',
    'author': 'proxe',
    'version': (0, 1, '0'),
    'blender': (2, 93),
    'location': 'System Console',
    'category': 'Development'}


import os
import sys
import time

import bpy
import addon_utils


timestamps = {}
addons = []


def on_change():
    reload = ()

    for addon in addon_utils.modules():
        path = addon.__file__
        name = addon.__name__

        if not addon_utils.check(name)[0] and name not in addons:
            continue

        for root, dirs, files in os.walk(os.path.dirname(path)):
            for file in files:
                if not file.endswith('.py'):
                    continue

                _path = os.path.join(root, file)
                new_module = False

                if _path not in timestamps:
                    timestamps[_path] = os.path.getmtime(_path)
                    new_module = name in addons

                if os.path.getmtime(_path) == timestamps[_path] and not new_module:
                    continue

                timestamps[_path] = os.path.getmtime(_path)

                separator = os.path.sep
                module = F'{root}{separator}{file}'.split(name)[-1].replace(separator, '.')[1:-3].rstrip()
                reload = (addon, module if module else '__main__')

        if name in addons:
            continue

        addons.append(name)

    if not reload:
        return 1.0

    print(F'\nChanges detected in "{reload[0].__name__}", reloading...')
    print(F'Changed module: {reload[1]}')
    time_start = time.perf_counter()

    try:
        bpy.ops.preferences.addon_disable(module=reload[0].__name__)

        count = 0
        for k in list(sys.modules.keys()):
            if k.startswith(reload[0].__name__):
                count += 1
                del sys.modules[k]

        print(F'Purged {count} addon modules')

        try:
            bpy.ops.preferences.addon_enable(module=reload[0].__name__)
            print(F'Reload successfull ({time.perf_counter() - time_start:.2f} seconds)')
        except:
            print(F'\nFailed to enable {reload[0].__name__}')

    except:
        print(F'\nFailed to reload {reload[0].__name__}')

    print()

    return 1.0


def register():
    if not bpy.app.timers.is_registered(on_change):
        bpy.app.timers.register(on_change, first_interval=1.0)


def unregister():
    if bpy.app.timers.is_registered(on_change):
        bpy.app.timers.unregister(on_change)

