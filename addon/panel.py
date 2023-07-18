from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class ADU_PT_tools(Panel):
    bl_label = "Addon"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Dev"


    def draw(self, context):
        wm = context.window_manager
        packaging = wm.adu.packaging
        layout = self.layout

        column = layout.column(align=True)

        #TODO: list of recently changed addons (populates packaging.source on active index change)

        column.operator('adu.create_zip')

        column.prop(packaging, 'source', text='')
        column.prop(packaging, 'destination', text='')


class ADU_PT_reload(Panel):
    bl_label = "Reload"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Dev"
    bl_options = {'DEFAULT_CLOSED'}

    bl_parent_id = 'TEXT_PT_tools'


    def draw(self, context):
        layout = self.layout

        layout.label(text='here')


class ADU_PT_packaging(Panel):
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
    ADU_PT_tools,
    # ADU_PT_reload,
    # ADU_PT_packaging,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

