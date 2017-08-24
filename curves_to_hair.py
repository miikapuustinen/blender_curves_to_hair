bl_info = {
        "name": "Copy Curves to Particles",
        "author": "Miika Puustinen",
        "description": "Copy curves to hair particles.",
        "version": (0, 0, 1),
        "blender": (2, 78, 0),
        "location": "View3D > Space > Copy Curves to Particles",
        "warning": "This very hackish. Use it with your own risk",
        "category": "3D View"
        }

import bpy


class copy_curves_to_particles(bpy.types.Operator):
    bl_idname = "object.copy_curves_to_particles"
    bl_label = "Copy Curves to Particle Hair"
    
    
    def execute(self, context):


        #Here the magic happens
        def copy_hair(hair_object, curve_object):
            psys = hair_object.particle_systems.active
            particles = psys.particles
            splines = curve_object.data.splines

            print("Copying " + str(len(splines)) + " curves to hair particles")

            psys.settings.hair_step = len(splines[0].points) -1
            psys.settings.count = len(splines)
            bpy.context.scene.update()
            for i, (particle, spline) in enumerate(zip(particles, splines)):
                for j, (hair_key, point)  in enumerate(zip(particle.hair_keys, spline.points)):
                    particle.hair_keys[j].co[0] = spline.points[j].co[0]
                    particle.hair_keys[j].co[1] = spline.points[j].co[1]
                    particle.hair_keys[j].co[2] = spline.points[j].co[2]
                 
            original_type = bpy.context.area.type
            bpy.context.area.type = "VIEW_3D"

            bpy.ops.particle.particle_edit_toggle()
            bpy.context.scene.tool_settings.particle_edit.select_mode = 'POINT'
            bpy.ops.particle.select_all(action='SELECT')
            bpy.ops.transform.resize(value=(1, 1, 1))

            bpy.ops.particle.particle_edit_toggle()

            bpy.context.area.type = original_type 
            


        sel = bpy.context.selected_objects

        #Check if active object is hair object and second object curves
        if len(sel) == 2:
            active =  bpy.context.active_object
            if  active == sel[0] and sel[0].type == 'MESH' and len(sel[0].particle_systems) >= 1 and sel[0].particle_systems.active.settings.type == 'HAIR':
                if sel[1].type == 'CURVE':
                    hair_object = sel[0]
                    curve_object = sel[1]
                    copy_hair(hair_object, curve_object)

            elif active == sel[1] and sel[1].type == 'MESH' and len(sel[1].particle_systems) >= 1 and sel[1].particle_systems.active.settings.type == 'HAIR':
                if sel[0].type == 'CURVE':
                    hair_object = sel[1]
                    curve_object = sel[0]
                    copy_hair(hair_object, curve_object)

            else:
                print("Active object must have hair particles. Selefted object needs to be a curve object!")
        else:
            print("Select Curve object and Particle Hair object!")
                    

             


        return {'FINISHED'}
    
    
    



def register():
    bpy.utils.register_class(copy_curves_to_particles)


def unregister():
    bpy.utils.unregister_class(copy_curves_to_particles)


 
if __name__ == "__main__":  
    register()


