from bpy.types import AddonPreferences, PropertyGroup, WindowManager
from bpy.props import PointerProperty, StringProperty
from bpy.utils import register_class, unregister_class

from . path import sep


class preference(AddonPreferences):
    bl_idname = __package__.split('.')[0]

    # format_console
    # reload modules
    # reload bl_ui


class packaging(PropertyGroup):
    source: StringProperty( #TODO: validate
        name = "Source Path",
        description = "Path to the source directory",
        subtype = 'DIR_PATH',
        default = F'addon{sep}path')

    destination: StringProperty( #TODO: validate
        name = "Destination Path",
        description = "Path to the destination directory",
        subtype = 'DIR_PATH',
        default = F'zip{sep}save{sep}path')

    # remove copy
    # use version
    # insert license
      # all/init only
      # full/snub
    # debug blocks
      # disable/remove (from commented debug to commented end or end of scope '\n')
    # remove comments


class property(PropertyGroup):
    packaging: PointerProperty(
        type = packaging,
        name = "Packaging",
        description = "Packaging properties")


classes = (
    preference,
    packaging,
    property,
)


def register():
    for cls in classes:
        register_class(cls)

    WindowManager.adu = PointerProperty(type=property)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    del WindowManager.adu

