bl_info = {
    "name": "Smash Hit Complex Wall Constructor",
    "author": "Happy_mimimix",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "View3D > Object > Mesh To Smash Hit Walls",
    "category": "Object"
}

import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (IntProperty)

class OBJECT_OT_voxelize(Operator):
    bl_label = "Mesh -> Smash Hit Walls"
    bl_idname = "object.voxelize"
    bl_description = "Convert complex mesh into multiple tiny cubes that are understandable by Smash Hit."
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    resolution: bpy.props.IntProperty(
        name = "Resolution",
        default = 16,
        min = 1
    )
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object and context.object.type == 'MESH'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        target_obj = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        target_obj.select_set(True)
        bpy.context.view_layer.objects.active = target_obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        bpy.ops.mesh.primitive_cube_add()
        base_unit = bpy.context.active_object
        base_unit.name = target_obj.name
        bpy.ops.object.select_all(action='DESELECT')
        target_obj.select_set(True)
        bpy.context.view_layer.objects.active = target_obj
        cube_size = max(target_obj.dimensions) / (self.resolution*2)

        bpy.context.scene.frame_set(0)
        wall_constructor = target_obj.modifiers.new(name='sh_wall_constructor',type='PARTICLE_SYSTEM')
        psettings = wall_constructor.particle_system.settings
        psettings.count = 0
        psettings.frame_start = 0
        psettings.frame_end = 0
        psettings.lifetime = 1
        psettings.lifetime_random = 0
        psettings.emit_from = 'FACE'
        psettings.use_modifier_stack = True
        psettings.distribution = 'GRID'
        psettings.invert_grid = False
        psettings.hexagonal_grid = False
        psettings.grid_resolution = 1
        psettings.grid_random = 0
        psettings.normal_factor = 0
        psettings.tangent_factor = 0
        psettings.object_align_factor = [0,0,0]
        psettings.object_factor = 0
        psettings.factor_random = 0
        psettings.use_rotations = False
        psettings.physics_type = 'NO'
        psettings.render_type = 'OBJECT'
        psettings.particle_size = cube_size
        psettings.instance_object = base_unit
        psettings.use_global_instance = False
        psettings.use_rotation_instance = False
        psettings.use_scale_instance = False
        psettings.use_parent_particles = False
        psettings.show_unborn = False
        psettings.use_dead = False
        psettings.display_method = 'RENDER'
        psettings.display_color = 'MATERIAL'
        psettings.display_percentage = 100
        psettings.child_type = 'NONE'
        psettings.use_self_effect = False
        psettings.force_field_1.type = 'NONE'
        psettings.force_field_2.type = 'NONE'
        psettings.grid_resolution = self.resolution
        bpy.ops.object.duplicates_make_real()
        bpy.data.objects.remove(target_obj, do_unlink=True)
        bpy.data.objects.remove(base_unit, do_unlink=True)
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_voxelize.bl_idname)
    
def register():
    bpy.utils.register_class(OBJECT_OT_voxelize)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_voxelize)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if __name__ == "__main__":
    register()
