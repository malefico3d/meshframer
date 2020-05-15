bl_info = {
    "name": "Meshframer",
    "author": "malefico3d@gmail.com",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "View3D",
    "description": "Creates new objects as mesh keyframes to simulate Stopmotion like animations.",
    "warning": "",
    "wiki_url": "",
    "category": "Animation"
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add


def create_meshframe():
    # Crea un objeto duplicado con nueva mesh, 
    # con nombre modificado segun el frame actual
    escena = bpy.context.scene
    objeto = bpy.context.active_object # El objeto activo
    frame_actual = escena.frame_current
    
    mesh = objeto.data

    dup_objeto = objeto.copy() #duplicamos objeto y sus coordenadas
    dup_objeto.data = mesh.copy()    
    
    nombre = objeto.name
    if nombre.find("_#") >= 0:
        nombre = nombre[:nombre.find("_#")] #Si encuentra estos caracteres es un frame creado por nosotros
    # Creamos en memoria el objeto y le asignamos la malla nueva
    dup_objeto.name = nombre + "_#" + str(frame_actual)

    # Cuando se copia el objeto tambie se copian su animation_data
    # el duplicado no debe heredar la animacion del original.

    if dup_objeto.animation_data :
        dup_objeto.animation_data_clear() #borra todos los keyframes anteriores.
    
    dup_objeto.hide_viewport = True
    dup_objeto.hide_render = True
    dup_objeto.keyframe_insert(data_path = "hide_viewport", frame=frame_actual - 1)
    dup_objeto.keyframe_insert(data_path = "hide_render", frame=frame_actual - 1)
    dup_objeto.hide_viewport = False
    dup_objeto.hide_render = False
    dup_objeto.keyframe_insert(data_path = "hide_viewport")
    dup_objeto.keyframe_insert(data_path = "hide_render")
    
    objeto.hide_viewport = False
    objeto.hide_render = False
    objeto.keyframe_insert(data_path = "hide_viewport", frame=frame_actual - 1)
    objeto.keyframe_insert(data_path = "hide_render", frame=frame_actual - 1)
    objeto.hide_viewport = True
    objeto.hide_render = True
    objeto.keyframe_insert(data_path = "hide_viewport")
    objeto.keyframe_insert(data_path = "hide_render")
    
    escena.collection.objects.link(dup_objeto) # Crea el objeto en la escena
    bpy.context.view_layer.objects.active = dup_objeto
        
def toggle_meshframe():
    objeto = bpy.context.active_object
    objeto.hide_viewport = not(objeto.hide_viewport)
    
    
class Meshframer_OT_Operator(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "view3d.meshframer"
    bl_label = "Meshframe"
    bl_description = "Creates a Meshframe"
    
    def execute(self, context):
        create_meshframe()
        return {'FINISHED'}

class Toggle_Meshframe_OT_Operator(bpy.types.Operator):
    """Toggles Meshframe Visibility"""
    bl_idname = "view3d.toggle_meshframe"
    bl_label = "Toggle Meshframe"
    bl_description = "Toggles Selected Meshframe"
    
    def execute(self, context):
        toggle_meshframe()
        return {'FINISHED'}

class Meshframer_PT_Panel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_meshframe"
    bl_label = "Add MeshFrame"
    bl_category = "Test Meshframe"
    bl_space_type= "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("view3d.meshframer", text="Create Meshframe")
        #col.operator("view3d.toggle_meshframe", text="Toggles Meshframe")
        

# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(Meshframer_OT_Operator)
   # bpy.utils.register_class(Toggle_Meshframe_OT_Operator)
    bpy.utils.register_class(Meshframer_PT_Panel)
    bpy.utils.register_manual_map(add_object_manual_map)
    


def unregister():
    bpy.utils.unregister_class(Meshframer_OT_Operator)
    # bpy.utils.unregister_class(Toggle_Meshframe_OT_Operator)
    bpy.utils.unregister_class(Meshframer_PT_Panel)
    bpy.utils.unregister_manual_map(add_object_manual_map)


if __name__ == "__main__":
    register()
