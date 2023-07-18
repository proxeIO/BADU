from . import property, operator, panel

modules = [
    property,
    operator,
    panel,
]


def register():
    for mdl in modules:
        mdl.register()


def unregister():
    for mdl in reversed(modules):
        mdl.unregister()

