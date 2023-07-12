from bpy.types import AddonPreferences, PropertyGroup
from bpy.utils import register_class, unregister_class


class preference(AddonPreferences):
    bl_idname = __package__.split('.')[0]

    # format_console
    # reload modules
    # reload bl_ui


class property(PropertyGroup):
    ...


classes = (
    preference,
    property,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)

