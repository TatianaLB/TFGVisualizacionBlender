import bpy
import json

RESCALE_FACTOR = 2 # x -> x/rescale
RESCALE_DIM = 3

# Create the Collection for Buildings
collection_buildings = bpy.data.collections.new('BUILDINGS')
bpy.context.collection.children.link(collection_buildings)
coll = bpy.data.scenes['Scene'].collection

# Read the JSON file
json_fname = bpy.path.abspath('//json/buildings.json')
with open(json_fname) as infile:
    data = json.load(infile)  

# Take the different buildings
json_colls = data['Buildings'] 

for building_info in json_colls: 
    #print(building_info)
    #print(building_info['type'])
    location_x = int(building_info['center_x']/RESCALE_FACTOR)
    location_y = int(building_info['center_y']/RESCALE_FACTOR)
    building_type = building_info['type']

    # Add a Building in Object Mode
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except RuntimeError:
        pass   
        
    if building_type == 'c0':
        
        file_full_path = '//objects_buildings/Vivienda.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Vivienda = bpy.context.object 

        Vivienda.location = (location_x, location_y, 0)
        Vivienda.dimensions = (25.9/RESCALE_FACTOR, 28.2/RESCALE_FACTOR, 21.3/RESCALE_FACTOR)
        collection_buildings.objects.link(Vivienda)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c1':

        file_full_path = '//objects_buildings/Hotel.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Hotel = bpy.context.object 

        Hotel.location = (location_x, location_y, 0)
        Hotel.dimensions = (54.6/4, 44.5/4, 66.4/4)
        collection_buildings.objects.link(Hotel)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c2':

        file_full_path = '//objects_buildings/Supermercado.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Supermercado = bpy.context.object 

        Supermercado.location = (location_x, location_y, 0)
        Supermercado.dimensions = (9.38/RESCALE_FACTOR, 8.71/RESCALE_FACTOR, 19.7/RESCALE_FACTOR)
        collection_buildings.objects.link(Supermercado)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
            
    elif building_type == 'c3':

        file_full_path = '//objects_buildings/CentroComercial.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        CentroComercial = bpy.context.object 
        CentroComercial.name = "Centro Comercial"

        CentroComercial.location = (location_x, location_y, 0)
        CentroComercial.dimensions = (62.5/RESCALE_DIM, 24.4/RESCALE_DIM, 28.7/RESCALE_DIM)
        collection_buildings.objects.link(CentroComercial)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
        
    elif building_type == 'c4':

        file_full_path = '//objects_buildings/Industria.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Industria = bpy.context.object 

        Industria.location = (location_x, location_y, 0)
        Industria.dimensions = (42.7/RESCALE_DIM, 50.5/RESCALE_DIM, 25/RESCALE_DIM)
        collection_buildings.objects.link(Industria)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
        
    elif building_type == 'c5': ###Revisar

        file_full_path = '//objects_buildings/Oficina.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Oficina = bpy.context.object 

        Oficina.location = (location_x, location_y, 0)
        Oficina.dimensions = (39.9/RESCALE_DIM, 13.3/RESCALE_DIM, 18.7/RESCALE_DIM)
        collection_buildings.objects.link(Oficina)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')   
        
    elif building_type == 'c6':

        file_full_path = '//objects_buildings/Escuela.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Escuela = bpy.context.object 
        Escuela.name = "Escuela"

        Escuela.location = (location_x, location_y, 0)
        Escuela.dimensions = (131/4, 27.3/4, 90.1/4)
        collection_buildings.objects.link(Escuela)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
        
    elif building_type == 'c7':

        file_full_path = '//objects_buildings/Biblioteca.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Biblioteca = bpy.context.object 

        Biblioteca.location = (location_x, location_y, 0)
        Biblioteca.dimensions = (27.2/RESCALE_DIM, 13.3/RESCALE_DIM, 35.1/RESCALE_DIM)
        collection_buildings.objects.link(Biblioteca)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
         
    elif building_type == 'c8':

        file_full_path = '//objects_buildings/Museo.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Museo = bpy.context.object 

        Museo.location = (location_x, location_y, 0)
        Museo.dimensions = (42/RESCALE_DIM, 10.9/RESCALE_DIM, 44/RESCALE_DIM) 
        collection_buildings.objects.link(Museo)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c13':

        file_full_path = '//objects_buildings/Restaurante.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Restaurante = bpy.context.object 

        Restaurante.location = (location_x, location_y, 0)
        Restaurante.dimensions = (175/RESCALE_DIM, 10/RESCALE_DIM, 36.5/RESCALE_DIM)
        Restaurante.rotation_euler[2] = 1.570796
        collection_buildings.objects.link(Restaurante)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection') 
        
    elif building_type == 'c14':

        file_full_path = //objects_buildings/Gimnasio.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Gimnasio = bpy.context.object 

        Gimnasio.location = (location_x, location_y, 0)
        Gimnasio.dimensions = (15.02/RESCALE_FACTOR, 8.05/RESCALE_FACTOR, 18.4/RESCALE_FACTOR)
        collection_buildings.objects.link(Gimnasio)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c15':

        file_full_path = '//objects_buildings/Bar.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Bar = bpy.context.object 

        Bar.location = (location_x, location_y, 0)
        Bar.dimensions = (21.1/RESCALE_FACTOR, 4.76/RESCALE_FACTOR, 9.02/RESCALE_FACTOR)
        collection_buildings.objects.link(Bar)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
           
    elif building_type == 'c16':

        file_full_path = '//objects_buildings/Teatro.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Teatro = bpy.context.object 

        Teatro.location = (location_x, location_y, 0)
        Teatro.dimensions = (32.5/RESCALE_DIM, 18.1/RESCALE_DIM, 60.5/RESCALE_DIM)
        collection_buildings.objects.link(Teatro)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c17':  
        
        file_full_path = '//objects_buildings/Estadio2.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Estadio = bpy.context.object 
        Estadio.name = "Estadio"

        Estadio.location = (location_x, location_y, 0)
        Estadio.dimensions = (35/RESCALE_DIM, 13.5/RESCALE_DIM, 40/RESCALE_DIM)
        collection_buildings.objects.link(Estadio)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')  
        
    elif building_type == 'c29':
        
        file_full_path = '//objects_buildings/Hospital2.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Hospital = bpy.context.object 
        Hospital.name = "Hopital"

        Hospital.location = (location_x, location_y, 0)
        Hospital.dimensions = (53.6/RESCALE_DIM, 21.8/RESCALE_DIM, 37.7/RESCALE_DIM)
        Hospital.rotation_euler[2] = 1.570796
        collection_buildings.objects.link(Hospital)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
    
    elif building_type == 'c28':  

        file_full_path = '//objects_buildings/MarquesinaBus.obj'
        #bpy.ops.import_scene.fbx(filepath=file_full_path)
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Marquesina = bpy.context.object 

        Marquesina.location = (location_x, location_y, 0)
        Marquesina.dimensions = (5/RESCALE_FACTOR, 3/RESCALE_FACTOR, 3/RESCALE_FACTOR)
        collection_buildings.objects.link(Marquesina)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c27':

        file_full_path = '//objects_buildings/Estacion.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Estacion = bpy.context.object 

        Estacion.location = (location_x, location_y, 0)
        Estacion.dimensions = (52.6/RESCALE_FACTOR, 13.4/RESCALE_FACTOR, 29.6/RESCALE_FACTOR)
        Estacion.rotation_euler[2] = 3.141593
        collection_buildings.objects.link(Estacion)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c31':  
        
        file_full_path = '//objects_buildings/Parking.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Aparcamiento = bpy.context.object 

        Aparcamiento.location = (location_x, location_y, 0)
        Aparcamiento.dimensions = (40/RESCALE_DIM, 15/RESCALE_DIM, 50/RESCALE_DIM)
        Aparcamiento.rotation_euler[2] = 3.141593
        collection_buildings.objects.link(Aparcamiento)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')  
        
    elif building_type == 'c35': 
    
        file_full_path = '//objects_buildings/Parque2.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Parque = bpy.context.object 

        Parque.location = (location_x, location_y, 0)
        Parque.dimensions = (16.8, 11, 15.7)
        Parque.rotation_euler[2] = 3.141593
        collection_buildings.objects.link(Parque)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')
        
    elif building_type == 'c36': 
    
        file_full_path = '//objects_buildings/Bomberos.obj'
        bpy.ops.wm.obj_import(filepath=file_full_path)
        Bomberos = bpy.context.object 

        Bomberos.location = (location_x, location_y, 0)
        Bomberos.dimensions = (46.2/RESCALE_FACTOR, 9.03/RESCALE_FACTOR, 26.4/RESCALE_FACTOR)
        collection_buildings.objects.link(Bomberos)
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')    
        
        
    else:
               
        bpy.ops.btools.add_floorplan()

        # Set the Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.btools.add_floors()

        bpy.ops.mesh.select_mode(type='FACE')
        edificio_obj = bpy.context.active_object
        edificio_obj.name = 'Edificio_' + str(building_info['id'])
        edificio_obj.location = (location_x, location_y, 0)
        edificio_obj.scale = (1,1,1)
           
        collection_buildings.objects.link(edificio_obj)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.collection.objects_remove(collection = 'Scene Collection')



