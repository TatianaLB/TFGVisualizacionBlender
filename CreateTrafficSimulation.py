import bpy
import xml.etree.ElementTree as ET
from random import randint
import datetime
from math import atan, degrees, radians, acos


def calculate_angle(x_diff, y_diff, previous_angle):
    # Depending on the values of the differences
    if x_diff == 0 and y_diff > 0:
        angle = -270
    if x_diff == 0 and y_diff < 0:
        angle = -90
    if x_diff > 0 and y_diff == 0:
        angle = 0
    if x_diff < 0 and y_diff == 0:
        angle = -180
    if x_diff > 0 and y_diff > 0:
        if previous_angle < 0:
            angle = -270 - degrees(atan(x_diff/y_diff))
        else:
            angle = 90 - degrees(atan(x_diff/y_diff))
    if x_diff < 0 and y_diff < 0:
        angle = -90 - degrees(atan(x_diff/y_diff))
    if x_diff > 0 and y_diff < 0:
        angle = -90 - degrees(atan(x_diff/y_diff))
    if x_diff < 0 and y_diff > 0:
        if previous_angle < 0:
            angle = -270 - degrees(atan(x_diff/y_diff))
        else:
            angle = 90 - degrees(atan(x_diff/y_diff))
    return angle


RESCALE_FACTOR = 2  # x -> x/rescale

# Extracts the tree root from the .xml
traffic_simulation_path = "//aimsunresults/aimsun_results_8058.xml"
root_traffic = ET.parse(traffic_simulation_path).getroot()

# The static element of xml
traffic = root_traffic[1]
print(len(traffic))

# Initializes data structures as a vehicle record
vehicles = dict()

# Crear un vector de objetos para los coches
car_objects = []

# Creamos una colección nueva para los coches
collection_cars = bpy.data.collections.new('CARS')
bpy.context.collection.children.link(collection_cars)

# Defines the interval of frames
frames = range(0, len(traffic))

# Set the frames of the Scene
bpy.data.scenes["Scene"].frame_start = 0
# bpy.data.scenes["Scene"].frame_end = 40
bpy.data.scenes["Scene"].frame_end = len(traffic)

for frame in frames:
    # Defines the range of event list for each frame
    events = range(0, len(traffic[frame]))

    # FRAME
    frame_time_str = traffic[frame].attrib['TIME']
    frame_time = datetime.datetime.strptime(
        frame_time_str, '%H:%M:%S.%f').time()
    frame_seconds = (datetime.timedelta(hours=frame_time.hour, minutes=frame_time.minute, seconds=frame_time.second, microseconds=frame_time.microsecond)
                     - datetime.timedelta(hours=0, minutes=0, seconds=0, microseconds=0)).total_seconds()

    # Iterates for each event in a frame (CREATED,CHANGED,DELETED)
    for event in events:
        # Defines the range of event list for each frame
        vehs = range(0, len(traffic[frame][event]))

        # Iterates for each vehicle in an event
        for veh in vehs:
            # Obtiene el ID del vehículo. Por ejemplo: 'vehículo 10000005'
            vehicle_id = int(traffic[frame][event][veh].attrib['ID'])

            # The vehicle has been created in this frame
            if traffic[frame][event].tag == 'CREATED':
                # The data position in this case is 5
                data = traffic[frame][event][veh][5].attrib
                # Gets the location in x,z coordinates of that vehicle and introduces them in the dictionary
                x = int(float(data['X1'])/RESCALE_FACTOR)
                y = int(float(data['Y1'])/RESCALE_FACTOR)
                # Generates a random color for vehicle (horse variant)
                color = randint(0, 9)
                # Introduces them in dictionary
                vehicles[vehicle_id] = {
                    "x0": x, "y0": y, "color": color, "change": 0, "angle": 0}

                # bpy.ops.mesh.primitive_cube_add()
                if color == 0:
                    file_full_path = '//objects_cars/BlueCar2.obj'
                elif color == 1:
                    file_full_path = '//objects_cars/BlackCar.obj'
                elif color == 2:
                    file_full_path = '//objects_cars/CianCar.obj'
                elif color == 3:
                    file_full_path = '//objects_cars/GreenCar.obj'
                elif color == 4:
                    file_full_path = '//objects_cars/OrangeCar.obj'
                elif color == 5:
                    file_full_path = '//objects_cars/PinkCar.obj'
                elif color == 6:
                    file_full_path = '//objects_cars/PurpleCar.obj'
                elif color == 7:
                    file_full_path = '//objects_cars/RedCar.obj'
                elif color == 8:
                    file_full_path = '//objects_cars/YellowCar.obj'
                else:
                    file_full_path = '//objects_cars/WhiteCar.obj'

                imported_obj = bpy.ops.wm.obj_import(filepath=file_full_path)
                car_obj = bpy.context.active_object
                # coche_obj.name = "Coche" + str(vehicle_id)
                car_obj.name = f"Car{vehicle_id}"
                # car_obj.rotation_euler[2]=3.141593
                # material = car_obj.active_material
                # material.node_tree.nodes['ShaderNodeBsdfPrincipled'].input[0].default_value = [0.800000, 0.472508, 0.000000, 1.000000]
                # Metemos el objeto en el vector
                car_objects.append(car_obj)

                # Agrega una propiedad "ID" a cada objeto de cubo
                car_obj["ID"] = vehicle_id

                # Metemos el objeto Car en una la colección de CARS
                collection_cars.objects.link(car_obj)
                bpy.ops.collection.objects_remove(
                    collection='Scene Collection')

                # Establecer la localización del coche en ese frame
                car_obj.location = (x, y, 0)
                car_obj.keyframe_insert(
                    data_path="location", frame=frame_seconds, index=-1)

            # The vehicle position has changed
            elif traffic[frame][event].tag == 'CHANGED':
                # The data position in this case is 0
                data = traffic[frame][event][veh][0].attrib

                # Gets the actual location
                x0 = vehicles[vehicle_id]["x0"]
                y0 = vehicles[vehicle_id]["y0"]
                previous_angle = vehicles[vehicle_id]["angle"]
                print(previous_angle)
                # Gets the location in x,z coordinates of that vehicle
                # Reads the new location in x
                x1 = int(float(data['X1'])/RESCALE_FACTOR)
                # Reads the new location in z
                y1 = int(float(data['Y1'])/RESCALE_FACTOR)

                # Calculates the angle
                x_diff = x1 - x0
                y_diff = y1 - y0

                angle = calculate_angle(x_diff, y_diff, previous_angle)

                # Updates entry
                vehicles[vehicle_id]["x1"] = x1
                vehicles[vehicle_id]["y1"] = y1
                vehicles[vehicle_id]["angle"] = angle

                vehicles[vehicle_id]["change"] = int(
                    vehicles[vehicle_id]["change"]) + 1

                for car_obj in car_objects:
                    if car_obj["ID"] == vehicle_id:
                        # Set the location of the car in that frame
                        car_obj.location = (x1, y1, 0)
                        car_obj.keyframe_insert(
                            data_path="location", frame=frame_seconds, index=-1)
                        car_obj.rotation_euler[2] = radians(angle)
                        car_obj.keyframe_insert(
                            data_path="rotation_euler", frame=frame_seconds, index=-1)

            # The vehicle has been removed in this frame
            elif traffic[frame][event].tag == 'DELETED':
                # Removes the key and value of the vehicle id from dictionary
                vehicles.pop(vehicle_id, None)
                # In case you want to remove the car from the scene:
                """for car_obj in car_objects:
                    if car_obj["ID"] == vehicle_id:
                        bpy.data.objects.remove(car_obj)""" 
                
            
           
