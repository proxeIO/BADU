from bpy.types import AddonPreferences, PropertyGroup, WindowManager
from bpy.props import PointerProperty, EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class

from . path import sep


class preference(AddonPreferences):
    bl_idname = __package__.split('.')[0]

    # format_console
    # reload modules
    # reload bl_ui


class packaging(PropertyGroup):
    addon: EnumProperty(
        name = "Addon to Package",
        description = "The addon to package",
        items = available_addons)

    destination: StringProperty( #TODO: validate
        name = "Destination Path",
        description = "Path to the destination directory",
        options = {'OUTPUT_PATH'},
        subtype = 'DIR_PATH',
        default = F'zip{sep}save{sep}dir')

    # remove copy
    # use version
    # insert license
      # all/init only
      # full (from LICENSE) /snub (from addon's __init__)
    # debug blocks
      # disable/remove (from commented debug to commented end or end of scope '\n' [tracking indentation])
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

