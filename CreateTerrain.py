import bpy

RESCALE_FACTOR = 2 # x -> x/rescale

# Create a collection to keep the terrain
collection_terrain = bpy.data.collections.new('TERRAIN')
bpy.context.collection.children.link(collection_terrain)

bpy.ops.mesh.primitive_plane_add()
terrain_obj = bpy.context.object
# Dimensions: Camera width = 1280 & Camera height = 720
camera_width = 1280
camera_height = 720
terrain_obj.dimensions = (camera_width/RESCALE_FACTOR,camera_height/RESCALE_FACTOR,0)
# Location should be half the dimensions
terrain_obj.location = (camera_width/(2*RESCALE_FACTOR),camera_height/(2*RESCALE_FACTOR),-0.5)
terrain_obj.name = "Terrain"

# Link the terrain to its collection
collection_terrain.objects.link(terrain_obj)
bpy.ops.collection.objects_remove(collection = 'Scene Collection')

###################################################################################
############################## TERRAIN SHAPE ######################################
###################################################################################

# Create a new particle system
particle_obj = terrain_obj.modifiers.new("Particles", 'PARTICLE_SYSTEM')

# Access the particle system settings
settings = particle_obj.particle_system.settings

# Set the type of particles
settings.type = 'HAIR'

# Set the number of particles
settings.count = 20000

# Set the Hair Length
settings.hair_length = 0.4

# Set where to emit particles from
settings.emit_from = "VOLUME"

# Set the distribution of particles random
settings.distribution = "RAND"

# Create child particles 
settings.child_type = "INTERPOLATED"

# Set the number of children per parent
settings.child_nbr = 20

#Set the number of children per parent for rendering
settings.rendered_child_count = 20

# Set the length of child paths
settings.child_length = 0.8

# Amount of particles left untouched by child path length: 
# different length from parent to generate more random
settings.child_length_threshold = 0.6

# Amount of clumping: to unit (or to separate) different paths
settings.clump_factor = -0.35

# Set the shape of clumping
settings.clump_shape = 0.7

# Edit Roughness
# Uniform
settings.roughness_1 = 0.01
# Size
settings.roughness_1_size = 0.072

###################################################################################
########################### TERRAIN MATERIAL ######################################
###################################################################################

# Create a new material for the Terrain
terrain_material = bpy.data.materials.new("TerrainMaterial")

# Assign the material to the terrain
terrain_obj.data.materials.append(terrain_material)

# Allow the use of nodes
terrain_material.use_nodes = True # Very important, otherwise it doesn't work
# Get the material's node tree
node_tree = terrain_material.node_tree 

# Clear the node tree
for node in node_tree.nodes:
    node_tree.nodes.remove(node)

# Add a Principled BSDF node
principled_node = node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
principled_node.location = (1700, 0)

# Add a Material Output node
output_node = node_tree.nodes.new(type="ShaderNodeOutputMaterial")
output_node.location = (2000,0)

# Link the nodes together
node_tree.links.new(principled_node.outputs[0], output_node.inputs[0]) 

# Add an Object Info node
object_info_node = node_tree.nodes.new(type="ShaderNodeObjectInfo")
object_info_node.location = (1000,0)

# Add a Color Ramp node
color_ramp_node = node_tree.nodes.new(type="ShaderNodeValToRGB")
color_ramp_node.color_ramp.elements[0].position = 0.89
color_ramp_node.color_ramp.elements[0].color = [0.180275, 0.290504, 0.000099, 1.000000]
color_ramp_node.location = (1300,0)

# Link the nodes together
node_tree.links.new(object_info_node.outputs[5], color_ramp_node.inputs[0])
node_tree.links.new(color_ramp_node.outputs[0], principled_node.inputs[0])

