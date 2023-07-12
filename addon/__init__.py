from . import property, operator

modules = [
    property,
    operator,
]


def register():
    for mdl in modules:
        mdl.register()


def unregister():
    for mdl in modules:
        mdl.unregister()

