from bpy.types import Operator
from bpy.utils import register_class, unregister_class

# symlink

class ADU_OT_create_zip(Operator):
    bl_idname = 'adu.create_zip'
    bl_label = "Package Addon"
    bl_description = "Create a zip archive of an addon"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        if not context:
            return False

        pkg = context.window_manager.adu.packaging
        return pkg.source not in {'', pkg.__annotations__['source'].keywords['default']} #TODO: use path.validate


    def execute(self, context):
        ...


classes = (
    ADU_OT_create_zip,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

