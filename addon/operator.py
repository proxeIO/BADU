from bpy.types import Operator
from bpy.utils import register_class, unregister_class

from . import property

# symlink

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
        from .. addon import name
        from . path import scripts, sep

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Copying\n    From: {src.replace(scripts, truncated)}\n    To:   {dst.replace(scripts, truncated)}")


    @staticmethod
    def clean(dir):
        from .. addon import name
        from . path import scripts, sep

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Cleaning\n    Path: {dir.replace(scripts, truncated)}")


    @staticmethod
    def insert(dir):
        from .. addon import name
        from . path import scripts, sep

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Inserting info\n    Path: {dir.replace(scripts, truncated)}")


    @staticmethod
    def compress(dir, dst):
        from .. addon import name
        from . path import scripts, sep

        truncated = F"..{sep}addon{sep}scripts"
        print(F"  Archiving\n    Path: {dir.replace(scripts, truncated)}\n    In:   {dst.replace(scripts, truncated)}")


    def execute(self, context):
        import time
        time_start = time.perf_counter()

        import addon_utils

        from .. addon import name, preferences
        from . path import abspath, join, dirname, scripts, sep

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
                dst = join(_path, src)
                print(F"  No destination path specified, using addon directory...")

            else:
                dst = join(dst, src)

            src = _path

            break

        self.copy(src, dst)
        self.clean(dst)
        # self.insert(dst)

        zip = F"{_name}-{version}.zip"
        output = join(_path if pkg.destination in {'', property.reference(pkg, 'destination')} else pkg.destination, zip)
        self.compress(dst, output)

        #TODO: remove dst dir

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

