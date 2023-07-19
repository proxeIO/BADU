# Symlinked, registration failures here will result in loss of live reload functionality
# This may require manually enabling the live reload addon in preferences once corrected
bl_info = {
    'name': "Addon Dev Utils: Live Reload",
    'description': "Live reload enabled addons when a source change is detected.",
    'author': "proxe",
    'version': (0, 0, '1'), # Independent BADU version
    'blender': (2, 93),
    'location': "System Console",
    'category': 'Development'}


import os
import sys
import time

import bpy
import addon_utils


timestamps = {}
addons = []

scripts = os.path.join(bpy.utils.user_resource('SCRIPTS'), 'addons')


def on_change():
    reload = ()

    for addon in addon_utils.modules():
        if not addon.__file__.startswith(scripts):
            continue

        path = addon.__file__
        name = addon.__name__

        if not addon_utils.check(name)[0] and name not in addons:
            continue

        new_module = False
        for root, dirs, files in os.walk(os.path.dirname(path)):
            for file in files:
                if not file.endswith('.py'):
                    continue

                _path = os.path.join(root, file)

                if _path not in timestamps:
                    timestamps[_path] = os.path.getmtime(_path)
                    new_module = name in addons

                if os.path.getmtime(_path) == timestamps[_path] and not new_module:
                    continue

                timestamps[_path] = os.path.getmtime(_path)

                separator = os.path.sep
                module = F"{root}{separator}{file}".split(name)[-1].replace(separator, '.')[1:-3].rstrip()
                reload = (addon, module if module else '__main__')

        if name in addons:
            continue

        addons.append(name)

    if not reload:
        return 1.0

    import importlib

    init = importlib.import_module(reload[0].__name__)
    name = init.bl_info['name']

    print(F"\nChanges detected in '{name}', reloading...")
    print(F"  {'Changed' if not new_module else 'New'} module: {reload[1]}")
    time_start = time.perf_counter()

    try:
        bpy.ops.preferences.addon_disable(module=reload[0].__name__)

        count = 0
        for k in list(sys.modules.keys()):
            if k.startswith(reload[0].__name__):
                count += 1
                del sys.modules[k]

        print(F"  Purged {count} addon modules")

        try:
            bpy.ops.preferences.addon_enable(module=reload[0].__name__)
            print(F"Reload successfull ({time.perf_counter() - time_start:.2f} seconds)")
        except:
            print(F"\nFailed to enable {reload[0].__name__} (still monitoring)")

    except:
        print(F"\nFailed to reload {reload[0].__name__} (still monitoring)")

    print()

    return 1.0


def register():
    if not bpy.app.timers.is_registered(on_change):
        bpy.app.timers.register(on_change, first_interval=1.0)


def unregister():
    if bpy.app.timers.is_registered(on_change):
        bpy.app.timers.unregister(on_change)

