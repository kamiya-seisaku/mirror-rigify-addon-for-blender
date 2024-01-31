# Mirror Rigify Addon for Blender
# Made by kkey, 2023, with helps from ChatGPT.
#
# Hi there. You're totally free to use this script however you want.
# You can copy it, change it, or even make something new with it.
# Just have fun and maybe share what you make with others too!
#
# Remember, this is shared as-is, no guarantees. But I hope it works great for you!

import bpy

# Add-on information
bl_info = {
    "name": "Mirror Rigify",
    "author": "kkey",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > My Tab",
    "description": "Copies bone transformations from one Rigify armature to another.",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}

# Property group to hold the armature references
class MirrorRigifyProperties(bpy.types.PropertyGroup):
    # Source armature property with an eyedropper selector
    source_armature: bpy.props.PointerProperty(
        name="Source Rigify Armature",
        type=bpy.types.Object,
        description="Select the source Rigify armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    # Target armature property with an eyedropper selector
    target_armature: bpy.props.PointerProperty(
        name="Target Rigify Armature",
        type=bpy.types.Object,
        description="Select the target Rigify armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

# UI Panel in the 3D View
class MirrorRigifyPanel(bpy.types.Panel):
    bl_label = "Mirror Rigify"
    bl_idname = "OBJECT_PT_mirror_rigify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        props = context.scene.mirror_rigify_props

        # UI elements for selecting armatures
        layout.prop(props, "source_armature")
        layout.prop(props, "target_armature")
        # Button to execute the mirroring operation
        layout.operator("object.mirror_rigify")

# Operator to perform the mirroring action
class MirrorRigify(bpy.types.Operator):
    bl_idname = "object.mirror_rigify"
    bl_label = "Mirror Rigify"

    def execute(self, context):
        props = context.scene.mirror_rigify_props
        source_armature = props.source_armature
        target_armature = props.target_armature

        # Check if both armatures are selected
        if not source_armature or not target_armature:
            self.report({'ERROR'}, "Armatures not found")
            return {'CANCELLED'}

        # Ensure both armatures are in object mode before changes
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # Perform the mirroring operation
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode='EDIT')

        for bone in target_armature.data.edit_bones:
            if bone.name in source_armature.data.edit_bones:
                source_bone = source_armature.data.edit_bones[bone.name]
                bone.head = source_bone.head
                bone.tail = source_bone.tail
                # Skip copying 'roll' as discussed

        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

# Register and unregister functions for Blender to hook up the addon
def register():
    bpy.utils.register_class(MirrorRigifyProperties)
    bpy.utils.register_class(MirrorRigifyPanel)
    bpy.utils.register_class(MirrorRigify)
    bpy.types.Scene.mirror_rigify_props = bpy.props.PointerProperty(type=MirrorRigifyProperties)

def unregister():
    bpy.utils.unregister_class(MirrorRigifyProperties)
    bpy.utils.unregister_class(MirrorRigifyPanel)
    bpy.utils.unregister_class(MirrorRigify)
    del bpy.types.Scene.mirror_rigify_props

if __name__ == "__main__":
    register()
