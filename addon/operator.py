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

        packaging = context.window_manager.adu.packaging
        default = packaging.__annotations__['source'].keywords['default']
        source = packaging.source
        return source not in {'', default} #TODO: use validate


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

