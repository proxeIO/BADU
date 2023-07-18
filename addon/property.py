from bpy.types import AddonPreferences, PropertyGroup, WindowManager
from bpy.props import PointerProperty, EnumProperty, StringProperty
from bpy.utils import register_class, unregister_class

from . path import sep, scripts

known_addons = []


def reference(property_group, property, keyword='default'):
    return property_group.__annotations__[property].keywords[keyword]


def available_addons(self, context):
    if known_addons:
        return known_addons

    import addon_utils
    import importlib

    from .. addon import name, package

    for m in addon_utils.modules():
        if not addon_utils.check(m.__name__)[0] or not m.__file__.startswith(scripts) or name in m.__name__ or package == m.__name__:
            continue

        init = importlib.import_module(m.__name__)
        _name = str(init.bl_info['name'])

        known_addons.append((m.__name__, _name, ""))

    return known_addons if known_addons else [('NONE', '', "")]


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


class preference(AddonPreferences):
    bl_idname = __package__.split('.')[0]

    packaging: PointerProperty(
        type = packaging,
        name = "Packaging",
        description = "Packaging properties")

    # format_console
    # reload modules
    # reload bl_ui


    def draw(self, context):
        layout = self.layout

        layout.prop(self.packaging, 'addon')
        layout.prop(self.packaging, 'destination')


class property(PropertyGroup):
    ...


classes = (
    packaging,
    preference,
    # property,
)


def register():
    for cls in classes:
        register_class(cls)

    # WindowManager.adu = PointerProperty(type=property)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    # del WindowManager.adu

