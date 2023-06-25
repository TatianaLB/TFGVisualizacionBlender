import bpy
from mathutils import Vector
import json

RESCALE_FACTOR = 2 # x -> x/rescale

# Create a collection in which to link the roads
collection_roads = bpy.data.collections.new('ROADS')
bpy.context.collection.children.link(collection_roads)

# Create a collection to link the trajectories of the roads, the Bezier curves
collection_bezier = bpy.data.collections.new('BEZIER ROADS')
bpy.context.collection.children.link(collection_bezier)

json_fname = bpy.path.abspath('//json/roads_bezier.json')
# Open the file in json format
with open(json_fname) as infile:
    json_info = json.load(infile)  # Access the json info
    
    
# Iterate through each Road object
for road in json_info['Roads']:
    # Get the name of the Road object
    road_name = list(road.keys())[0]
    
    # Access Directions and Points data
    directions = road[road_name]['Directions']
    
    # Access the Direct and Reverse values ​​in the Directions object
    direct = road[road_name]['Directions']['Direct']
    reverse = road[road_name]['Directions']['Reverse']
    wide_road = direct + reverse
    
    # Access the list of points in the Points object
    point_list = road[road_name]['Points']
    points = []
    for point in point_list:
        vec = Vector((int(point[0]/RESCALE_FACTOR),int(point[1]/RESCALE_FACTOR),0))
        points.append(vec)
        
    # Create a new Bezier curve
    curve = bpy.data.curves.new('BezierCurve', 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 64

    # Create an empty object to contain the Bezier curve
    road_line_obj = bpy.data.objects.new('Bezier' + road_name, curve)
    collection_bezier.objects.link(road_line_obj)
    # Hide the Bezier lines of the final result
    road_line_obj.hide_viewport = True

    # Create a spline for the Bezier curve
    spline = curve.splines.new('BEZIER')

    # Set the points of the Bezier curve
    spline.bezier_points.add(len(points)-1)
    for i, point in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = point
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'    

    ######################################################################
    ##################### ROAD SHAPE WITH A PLANE ########################
    ######################################################################
    bpy.ops.mesh.primitive_plane_add()
    road_obj = bpy.context.object
    road_obj.name = road_name
    road_obj.location = (0,0,0)

    # The usual width of each lane is 3.50 meters
    y_dimension_road = wide_road*3.5
    road_obj.dimensions = (2,y_dimension_road,0)
    
    ###########################################################################################
    ################### Apply the modifiers to create the road along the path #################
    ###########################################################################################
    ### ARRAY Modifier
    bpy.ops.object.modifier_add(type='ARRAY')
    road_obj.modifiers["Array"].fit_type = "FIT_CURVE"
    road_obj.modifiers["Array"].curve = road_line_obj
    road_obj.modifiers["Array"].relative_offset_displace = (1,0,0)

    ### CURVE Modifier
    bpy.ops.object.modifier_add(type="CURVE")
    road_obj.modifiers["Curve"].object = road_line_obj
    road_obj.modifiers["Curve"].deform_axis = "NEG_Z"

    # The road must be rotated 90º in the Y axis
    # 90º = 1.570796 radians
    road_obj.rotation_euler = (0,1.570796,0)

    collection_roads.objects.link(road_obj)
    bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
    
    ############################################################
    #################### ROAD MATERIAL #########################
    ############################################################
    # Create a new material
    road_material = bpy.data.materials.new("RoadMaterial")

    # Add a material to the road
    road_obj.data.materials.append(road_material)

    # Allow the use of nodes
    road_material.use_nodes = True 
    # Get the material's node tree
    node_tree = road_material.node_tree 

    # Clear the node tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Add a Principled BSDF node
    principled_node = node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    # Location
    principled_node.location = (1700, 0)

    # Add a Material Output node
    output_node = node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    # Location
    output_node.location = (2000,0)

    # Link the nodes together
    node_tree.links.new(principled_node.outputs[0], output_node.inputs[0])


    # Add a Brick Texture node for continuous white lines
    bricktexturecont_node = node_tree.nodes.new(type="ShaderNodeTexBrick")
    bricktexturecont_node.offset_frequency = 1
    # Color1 & Color2: Road base color
    bricktexturecont_node.inputs[1].default_value = [0.000000, 0.000000, 0.000000, 1.000000]
    bricktexturecont_node.inputs[2].default_value = [0.000000, 0.000000, 0.000000, 1.000000]
    # Mortar: Color of the solid lines
    bricktexturecont_node.inputs[3].default_value = [0.800000, 0.800000, 0.800000, 1.000000]
    # Scale
    bricktexturecont_node.inputs[4].default_value = 5
    # Mortar Size: The width of the solid line
    bricktexturecont_node.inputs[5].default_value = 0.007
    # Mortar Smooth
    bricktexturecont_node.inputs[6].default_value = 0.2
    # Bias
    bricktexturecont_node.inputs[7].default_value = 0
    # Brick Width
    bricktexturecont_node.inputs[8].default_value = 11
    # Location
    bricktexturecont_node.location = (600, -200)
    
    # Create the center line when there is more than one lane
    if wide_road != 1:
        # Add a Brick Texture node for the center line
        bricktexturecenter_node = node_tree.nodes.new(type="ShaderNodeTexBrick")
        bricktexturecenter_node.offset_frequency = 1
        # Color1 & Color2: for the center line
        bricktexturecenter_node.inputs[1].default_value = [0.800000, 0.800000, 0.800000, 1.000000]
        bricktexturecenter_node.inputs[2].default_value = [0.800000, 0.800000, 0.800000, 1.000000]
        # Scale
        bricktexturecenter_node.inputs[4].default_value = 5
        # Mortar Size: The width of the center white line
        bricktexturecenter_node.inputs[5].default_value = 0.120
        # Mortar Smooth
        bricktexturecenter_node.inputs[6].default_value = 0.005
        # Location
        bricktexturecenter_node.location = (600, 200)

    # Add a Shader node Mix RGB for the two textures of the lines 
    mix_lines_node = node_tree.nodes.new(type="ShaderNodeMixRGB")
    # Location
    mix_lines_node.location = (800,0)
    # Activate this when there is only one lane
    if wide_road == 1:
        mix_lines_node.inputs[1].default_value = [0.000000, 0.000000, 0.000000, 1.000000]

    # Link the nodes together
    # Connect only when there is more than one lane
    if wide_road != 1:
        node_tree.links.new(bricktexturecenter_node.outputs[0], mix_lines_node.inputs[1])
    node_tree.links.new(bricktexturecont_node.outputs[0], mix_lines_node.inputs[2])

    # Add a Shader node Texture Coordinate
    texcoord_node = node_tree.nodes.new(type="ShaderNodeTexCoord")
    # Location
    texcoord_node.location = (200,0)

    # Add a Shader node Mapping
    mapping_node = node_tree.nodes.new(type="ShaderNodeMapping")    
    # Modify the center line with the x scale
    # and the number of lanes with y scale
    if wide_road != 1:
        y_scale = wide_road/40
        if (direct == 0) | (reverse == 0):
            x_scale = 0.1
        else:   
            x_scale = 0   
    elif wide_road == 1:
        y_scale = 0.05
        x_scale = 0    
    # Scale      
    mapping_node.inputs[3].default_value = (x_scale, y_scale, 1)
    # Location
    mapping_node.location = (400,0)

    # Link the nodes together
    node_tree.links.new(texcoord_node.outputs[2], mapping_node.inputs[0])
    # Connect only when there is more than one lane
    if wide_road != 1:
        node_tree.links.new(mapping_node.outputs[0], bricktexturecenter_node.inputs[0])
    node_tree.links.new(mapping_node.outputs[0], bricktexturecont_node.inputs[0])

    # Asphalt look generation
    # Add a Noise Texture
    noise_node = node_tree.nodes.new(type="ShaderNodeTexNoise")
    # Scale
    noise_node.inputs[2].default_value = 4.2
    # Detail
    noise_node.inputs[3].default_value = 16.0 
    # Location
    noise_node.location = (900,-300)
    
    # Add a Math Node, with operation add, for Roughness
    mathadd_node = node_tree.nodes.new(type="ShaderNodeMath")
    mathadd_node.operation = "ADD"
    mathadd_node.inputs[1].default_value = 0.2
    mathadd_node.location = (1450,-270)

    # Link the nodes together
    node_tree.links.new(noise_node.outputs[1], mathadd_node.inputs[0])
    node_tree.links.new(mathadd_node.outputs[0], principled_node.inputs[9])

    # Add a Color Ramp
    colorramp_node = node_tree.nodes.new(type="ShaderNodeValToRGB")
    colorramp_node.color_ramp.elements[0].position = 0.62
    colorramp_node.color_ramp.elements[0].color = [0.000000, 0.000000, 0.000000, 1.000000]
    # Location
    colorramp_node.location = (1100,-300)

    # Link the nodes together
    node_tree.links.new(noise_node.outputs[1], colorramp_node.inputs[0])

    # Add a Shader node Mix RGB for the texture lines and the noise
    mix_linesnoise_node = node_tree.nodes.new(type="ShaderNodeMixRGB")
    mix_linesnoise_node.inputs[0].default_value = 0.267
    # Location
    mix_linesnoise_node.location = (1400,-50)

    # Link the nodes together
    node_tree.links.new(mix_lines_node.outputs[0], mix_linesnoise_node.inputs[1])
    node_tree.links.new(colorramp_node.outputs[0], mix_linesnoise_node.inputs[2])
    node_tree.links.new(mix_linesnoise_node.outputs[0], principled_node.inputs[0])


    # Add real Asphalt texture with the Normal input from Principled BSDF
    # Add a Musgrave Texture Node
    musgrave_node = node_tree.nodes.new(type="ShaderNodeTexMusgrave")
    # Scale
    musgrave_node.inputs[2].default_value = 12.3
    # Detail
    musgrave_node.inputs[3].default_value = 10.6
    # Dimension
    musgrave_node.inputs[4].default_value = 0.4
    # Location
    musgrave_node.location = (1200, -600)

    # Add Bump node
    bump_node = node_tree.nodes.new(type="ShaderNodeBump")
    # Strength
    bump_node.inputs[0].default_value = 0.7
    bump_node.location = (1450, -600)

    # Link the nodes together
    node_tree.links.new(musgrave_node.outputs[0], bump_node.inputs[2])
    node_tree.links.new(bump_node.outputs[0], principled_node.inputs[22])

    ########################### END OF ROAD MATERIAL ############################
 

  
    
###########################################################################################
#################################### CROSSROADS ###########################################
###########################################################################################
    
# Create a collection to keep crossroads
collection_crossroads = bpy.data.collections.new('CROSSROADS')
bpy.context.collection.children.link(collection_crossroads)

# Get the file path with crossroads
json_fname = bpy.path.abspath('//json/crossroads.json')
# Open the JSON file
with open(json_fname) as file:
    json_data = json.load(file)  # Access the json information
    
    
# Iterate through each Crossroad object
for crossroad in json_data['Crossroads']:
    id = crossroad['id']
    center_x = int(crossroad['center_x']/RESCALE_FACTOR)
    center_y = int(crossroad['center_y']/RESCALE_FACTOR)
    in_directions = crossroad['in']
    out_directions = crossroad['out']
        
        
    ###########################################################################
    ##################### CROSSROAD SHAPE WITH A PLANE ########################
    ###########################################################################
        
    bpy.ops.mesh.primitive_plane_add()
    crossroad_obj = bpy.context.active_object
    crossroad_obj.location = (center_x,center_y,0.1)
    crossroad_obj.dimensions = (20, 20, 0)
    crossroad_obj.name = "Crossroad" + str(id)  
    
    # Modifier SUBSURF: to make the crossroads round
    bpy.ops.object.modifier_add(type='SUBSURF')    
    crossroad_obj.modifiers["Subdivision"].levels = 6  
    
    # Link the intersection to its collection
    collection_crossroads.objects.link(crossroad_obj)
    bpy.ops.collection.objects_remove(collection = 'Scene Collection')
      
    ############################################################
    #################### CROSSROAD MATERIAL ####################
    ############################################################
    # Create a new material
    crossroad_material = bpy.data.materials.new("CrossroadMaterial")

    # Add a material to the road
    crossroad_obj.data.materials.append(crossroad_material)

    # Allow the use of nodes
    crossroad_material.use_nodes = True 
    # Get the material's node tree
    node_tree = crossroad_material.node_tree 

    # Clear the node tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    # Add a Principled BSDF node
    principled_node = node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
    # Location
    principled_node.location = (1700, 0)

    # Add a Material Output node
    output_node = node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    # Location
    output_node.location = (2000,0)

    # Link the nodes together
    node_tree.links.new(principled_node.outputs[0], output_node.inputs[0]) 
    
    # Asphalt look generation
    # Add a Noise Texture
    noise_node = node_tree.nodes.new(type="ShaderNodeTexNoise")
    noise_node.inputs[2].default_value = 4.2
    noise_node.inputs[3].default_value = 16.0 
    noise_node.location = (900,-300)

    # Add a Color Ramp
    colorramp_node = node_tree.nodes.new(type="ShaderNodeValToRGB")
    colorramp_node.color_ramp.elements[0].position = 0.62
    colorramp_node.color_ramp.elements[0].color = [0.000000, 0.000000, 0.000000, 1.000000]
    colorramp_node.location = (1100,-300)

    # Link the nodes together
    node_tree.links.new(noise_node.outputs[1], colorramp_node.inputs[0])

    # Add a Shader node Mix RGB for the texture lines and the noise
    mix_linesnoise_node = node_tree.nodes.new(type="ShaderNodeMixRGB")
    mix_linesnoise_node.inputs[0].default_value = 0.267
    mix_linesnoise_node.inputs[1].default_value = [0.000000, 0.000000, 0.000000, 1.000000]
    mix_linesnoise_node.location = (1400,-50)

    # Link the nodes together
    node_tree.links.new(colorramp_node.outputs[0], mix_linesnoise_node.inputs[2])
    node_tree.links.new(mix_linesnoise_node.outputs[0], principled_node.inputs[0])

    # Add a Math Node, with operation add, for Roughness
    mathadd_node = node_tree.nodes.new(type="ShaderNodeMath")
    mathadd_node.operation = "ADD"
    mathadd_node.inputs[1].default_value = 0.2
    mathadd_node.location = (1450,-270)

    # Link the nodes together
    node_tree.links.new(noise_node.outputs[1], mathadd_node.inputs[0])
    node_tree.links.new(mathadd_node.outputs[0], principled_node.inputs[9])

    # Add real Asphalt texture with the Normal input from Principled BSDF
    # Add a Musgrave Texture Node
    musgrave_node = node_tree.nodes.new(type="ShaderNodeTexMusgrave")
    musgrave_node.inputs[2].default_value = 12.3
    musgrave_node.inputs[3].default_value = 10.6
    musgrave_node.inputs[4].default_value = 0.4
    musgrave_node.location = (1200, -600)

    # Add Bump node
    bump_node = node_tree.nodes.new(type="ShaderNodeBump")
    bump_node.inputs[0].default_value = 0.7
    bump_node.location = (1450, -600)

    # Link the nodes together
    node_tree.links.new(musgrave_node.outputs[0], bump_node.inputs[2])
    node_tree.links.new(bump_node.outputs[0], principled_node.inputs[22])

    ########################### END OF CROSSROAD MATERIAL ############################




       
