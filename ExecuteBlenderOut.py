import subprocess

# Ruta al ejecutable de Blender
ruta_blender = "C:/Program Files/Blender Foundation/Blender 3.3/blender.exe"
# Ruta al archivo .blend de Blender
ruta_archivo_blender = "//TFG Codigo Blender/CreateACity.blend"
# Ruta al archivo de Python dentro de Blender
ruta_archivo_python = "//CreateACityInBlender/CreateTerrain.py"
#ruta_archivo_python = "//CreateACityInBlender/CreateCrossroadsAndRoads.py"
#ruta_archivo_python = "//CreateACityInBlender/CreateBuildings.py"
#ruta_archivo_python = "//CreateACityInBlender/CreateTrafficSimulation.py"

# Comando para ejecutar Blender y el archivo de Python dentro de él
comando = [ruta_blender, ruta_archivo_blender, "--python", ruta_archivo_python]

# Ejecuta el comando
subprocess.call(comando)
