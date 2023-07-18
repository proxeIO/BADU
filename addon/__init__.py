from . import property, operator, panel

modules = [
    property,
    operator,
    panel,
]


def preferences(name=''):
    import bpy

    if not name:
        from .. addon import package as name

    return bpy.context.preferences.addons[name].preferences


def register():
    for mdl in modules:
        mdl.register()


def unregister():
    for mdl in reversed(modules):
        mdl.unregister()

