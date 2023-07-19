from bpy.types import Operator
from bpy.utils import register_class, unregister_class

from . import property


class ADU_OT_create_zip(Operator):
    bl_idname = 'adu.create_zip'
    bl_label = "Package Addon"
    bl_description = "Create a zip archive of given addon"
    bl_options = {'REGISTER', 'UNDO'}


    # @classmethod
    # def poll(cls, context):
    #     if not context:
    #         return False

    #     from .. addon import preferences
    #     pkg = preferences().packaging
    #     return pkg.addon not in {'', property.reference(pkg, 'addon')} #TODO: use path.validate


    @staticmethod
    def addon_name(mdl):
        import importlib

        init = importlib.import_module(mdl)
        name = str(init.bl_info['name'])

        return name


    @staticmethod
    def addon_version(mdl):
        import importlib

        init = importlib.import_module(mdl)
        version = str(init.bl_info['version']) \
          .replace(',', '.')                   \
          .replace(' ', '')                    \
          .replace('(', '')                    \
          .replace(')', '')                    \
          .replace("'", '')                    \
          .replace('"', '')                    \

        return version


    @staticmethod
    def copy(src, dst):
        from shutil import rmtree, copy2
        from os import readlink, remove, walk, makedirs

        from . path import scripts, sep, isdir, isfile, islink

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Copying\n    From: {src.replace(scripts, truncated)}\n    To:   {dst.replace(scripts, truncated)}\n")

        if islink(src):
            print("    SymLink detected, resolving...")
            src = readlink(src)

        if isdir(dst):
            print("    Destination directory exists, deleting...")
            rmtree(dst)

        elif isfile(dst):
            print("    Destination file exists, deleting...")
            remove(dst)

        files = []
        for root, dirs, _files in walk(src):
            basedir = root.replace(F"{src}{sep}", '')

            if basedir.startswith('.') or basedir.endswith('__'):
                print(F"    Ignoring {basedir}")

                continue

            _dirs = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]

            for dir in dirs:
                if dir not in _dirs:
                    print(F"    Ignoring {basedir}{sep}{dir}")

            __files = [f for f in _files if not f.endswith('.pyc') and not f.startswith('.')]

            for file in _files:
                if file not in __files:
                    print(F"    Ignoring {basedir}{sep}{file}")

            files.append((root, _dirs, __files))

        print()

        for root, dirs, _files in files:
            print(F"    Copying {root.replace(F'{src}{sep}', '')}")

            for dir in dirs:
                print(F"      Creating directory {dir}")

                _path = F"{root}{sep}{dir}"

                if islink(_path):
                    print(F"      SymLink detected, resolving...")
                    _path = readlink(_path)

                makedirs(_path.replace(src, dst))

            for file in _files:
                print(F"      Copying file {file}")

                _path = F"{root}{sep}{file}"

                if islink(_path):
                    print(F"      SymLink detected, resolving...")
                    _path = readlink(_path)

                copy2(_path, _path.replace(src, dst))


    @staticmethod
    def compress(src, dst):
        from os import remove
        from shutil import make_archive
        from . path import scripts, sep, isfile

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Archiving\n    Path: {src.replace(scripts, truncated)}\n    In:   {dst.replace(scripts, truncated)}")

        make_archive(dst, 'zip', src)


    def execute(self, context):
        import time
        time_start = time.perf_counter()

        import addon_utils

        from shutil import rmtree

        from .. addon import name, preferences
        from . path import abspath, join, dirname, scripts, sep, isfile, isdir

        pref = preferences()
        pkg = pref.packaging
        src = pkg.addon
        dst = pkg.destination

        _name = self.addon_name(src)
        version = self.addon_version(src)

        module = False
        _path = ''

        truncated = F"..{sep}addon{sep}scripts"

        for mdl in addon_utils.modules():
            if mdl.__name__ != src:
                continue

            module = '__init__' in mdl.__file__
            _path = dirname(mdl.__file__) if module else mdl.__file__
            print(F"{name}: Packaging Addon\n  Found '{_name}'\n    Path: {_path.replace(scripts, truncated)}")

            if dst in {'', property.reference(pkg, 'destination')}:
                dst = join(_path, src, src)
                print(F"  No destination path specified, using addon directory...")

            else:
                dst = join(dst, src, src)

            src = _path

            break

        zip = F"{_name}-{version}"
        output = join(_path if pkg.destination in {'', property.reference(pkg, 'destination')} else pkg.destination, zip)

        if isfile(output + '.zip'):
            self.report({'ERROR'}, F"Bump {_name} version OR delete existing ZIP archive:\n  {output}.zip")

            return {'CANCELLED'}

        self.copy(src, dst)
        self.compress(abspath(join(dst, '..')), output)

        cpy = abspath(join(dst, '..'))
        if isdir(cpy):
            rmtree(abspath(join(dst, '..')))
        else:
            remove(cpy)

        print(F"Packaged successfully ({time.perf_counter() - time_start:.2f} seconds)\n")

        self.report({'INFO'}, F"Packaged in {output}")

        return {'FINISHED'}


classes = (
    ADU_OT_create_zip,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

