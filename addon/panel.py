from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class BADU_PT_tools(Panel):
    bl_label = "Addon"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Dev"


    def draw(self, context):
        from .. addon import preferences
        pref = preferences()
        pkg = pref.packaging
        layout = self.layout

        column = layout.column(align=True)

        #TODO: list of recently changed addons (populates packaging.addon on active index change)
        box = column.box()
        box.scale_y = 0.5
        row = box.row(align=True)
        row.alignment = 'CENTER'
        row.label(text='Package Addon')

        column.prop(pkg, 'addon', text='')
        column.prop(pkg, 'destination', text='')
        column.operator('badu.create_zip')


class BADU_PT_reload(Panel):
    bl_label = "Reload"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Dev"
    bl_options = {'DEFAULT_CLOSED'}

    bl_parent_id = 'TEXT_PT_tools'


    def draw(self, context):
        layout = self.layout

        layout.label(text='here')


class BADU_PT_packaging(Panel):
    bl_label = "Packaging"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Dev"
    bl_options = {'DEFAULT_CLOSED'}

    bl_parent_id = 'TEXT_PT_tools'


    def draw(self, context):
        layout = self.layout

        layout.label(text='here')


classes = (
    BADU_PT_tools,
    # BADU_PT_reload,
    # BADU_PT_packaging,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

