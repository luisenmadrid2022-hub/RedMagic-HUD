import bpy
import math
import random

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Dimensiones
ANCHO_TOTAL = 10.0
LARGO_TOTAL = 10.2
ALTURA_TECHO = 2.8

# ============================================================
# UTILIDADES
# ============================================================
def crear_material(nombre, color, roughness=0.5, specular=0.5, metallic=0.0, emission=0.0, use_nodes=True):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = use_nodes
    if use_nodes:
        nodes = mat.node_tree.nodes
        principled = nodes.get('Principled BSDF')
        if principled:
            principled.inputs['Base Color'].default_value = (*color, 1.0)
            principled.inputs['Roughness'].default_value = roughness
            principled.inputs['Specular'].default_value = specular
            principled.inputs['Metallic'].default_value = metallic
            if emission > 0:
                principled.inputs['Emission Strength'].default_value = emission
                principled.inputs['Emission Color'].default_value = (*color, 1.0)
    return mat

def crear_caja(x, y, z, sx, sy, sz, color, roughness=0.5, specular=0.5, metallic=0.0, nombre="Caja", emission=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.object
    obj.scale = (sx/2, sy/2, sz/2)
    obj.name = nombre
    mat = crear_material(f"Mat_{nombre}", color, roughness, specular, metallic, emission)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def crear_pared(x, y, z, ancho, alto, profundidad, color=(0.97, 0.97, 0.95)):
    return crear_caja(x, y, z, ancho, alto, profundidad, color, roughness=0.8, nombre=f"Pared_{x}_{y}")

def crear_suelo(x, y, ancho, largo, color=(0.82, 0.78, 0.72)):
    return crear_caja(x, y, 0.05, ancho, largo, 0.1, color, roughness=0.6, nombre=f"Suelo_{x}_{y}")

def crear_ventanal(x, y, ancho, alto):
    crear_caja(x, y + 5.1, ALTURA_TECHO/2, ancho, 0.05, alto, (0.7, 0.85, 0.95), roughness=0.0, specular=1.0, nombre=f"Vidrio_{x}")
    crear_caja(x, y + 5.1, 0.1, ancho + 0.2, 0.08, 0.1, (0.3, 0.3, 0.3), roughness=0.5, nombre=f"Alfeizar_{x}")
    crear_caja(x, y + 5.1, 2.6, ancho + 0.2, 0.08, 0.1, (0.3, 0.3, 0.3), roughness=0.5, nombre=f"Dintel_{x}")

def crear_luz_area(x, y, z, potencia=500, color=(1.0, 0.95, 0.85), size=2.0):
    bpy.ops.object.light_add(type='AREA', location=(x, y, z))
    luz = bpy.context.object
    luz.data.energy = potencia
    luz.data.color = color
    luz.data.size = size
    luz.name = f"Luz_area_{x}_{y}"
    return luz

def crear_lampara_techo(x, y):
    crear_caja(x, y, ALTURA_TECHO - 0.05, 0.3, 0.3, 0.05, (0.8, 0.8, 0.8), metallic=0.8, nombre=f"Base_lampara_{x}_{y}")
    crear_caja(x, y, ALTURA_TECHO - 0.3, 0.15, 0.15, 0.5, (1.0, 0.95, 0.8), emission=2.0, nombre=f"Luz_lampara_{x}_{y}")

# Colores
COLOR_BLANCO = (0.95, 0.95, 0.93)
COLOR_SUELO = (0.82, 0.78, 0.72)
COLOR_PARED = (0.97, 0.97, 0.95)
COLOR_TECHO = (0.98, 0.98, 0.98)
COLOR_MADERA = (0.55, 0.35, 0.18)
COLOR_MADERA_CLARO = (0.7, 0.55, 0.35)
COLOR_MARMOL = (0.9, 0.88, 0.85)
COLOR_ACERO = (0.6, 0.6, 0.62)
COLOR_VIDRIO = (0.65, 0.8, 0.9)
COLOR_TELA = (0.75, 0.72, 0.68)
COLOR_VERDE = (0.2, 0.5, 0.2)
COLOR_AZULEJO = (0.85, 0.88, 0.9)

# ============================================================
# ESTRUCTURA BASE
# ============================================================
suelo_base = crear_caja(0, 0, -0.05, ANCHO_TOTAL, LARGO_TOTAL, 0.1, COLOR_SUELO, roughness=0.8, nombre="Suelo_base")

# Paredes exteriores
for y in [-5.1, 5.1]:
    crear_pared(0, y, ALTURA_TECHO/2, ANCHO_TOTAL, ALTURA_TECHO, 0.15)
for x in [-5, 5]:
    crear_pared(x, 0, ALTURA_TECHO/2, 0.15, ALTURA_TECHO, LARGO_TOTAL)

# Techos por estancias
crear_caja(1, 3.5, ALTURA_TECHO, 6, 6, 0.05, COLOR_TECHO, roughness=0.9, nombre="Techo_salon")
crear_caja(-2.5, 3.5, ALTURA_TECHO, 3.5, 4, 0.05, COLOR_TECHO, roughness=0.9, nombre="Techo_hab3")
crear_caja(4.5, -2.5, ALTURA_TECHO, 4, 4, 0.05, COLOR_TECHO, roughness=0.9, nombre="Techo_hab1")
crear_caja(4.5, 1, ALTURA_TECHO, 4, 3.5, 0.05, COLOR_TECHO, roughness=0.9, nombre="Techo_hab2")
crear_caja(-3, -2.5, ALTURA_TECHO, 2, 2, 0.05, COLOR_TECHO, roughness=0.9, nombre="Techo_bano")

# Paredes interiores
crear_pared(-2, -1.5, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 5)  # salon-pasillo
crear_pared(2.5, -1, ALTURA_TECHO/2, 4.5, ALTURA_TECHO, 0.12)  # pasillo-habs
crear_pared(4.5, -2.5, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 3)  # hab1-hab2
crear_pared(4.5, 1, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 3)    # hab2-bano

# Suelos por estancias (distintos colores)
crear_suelo(1, 3.5, 6, 6, COLOR_MADERA_CLARO)        # salon parquet
crear_suelo(-2.5, 3.5, 3.5, 4, COLOR_MADERA_CLARO)   # hab3
crear_suelo(4.5, -2.5, 4, 4, COLOR_MADERA_CLARO)     # hab1
crear_suelo(4.5, 1, 4, 3.5, COLOR_MADERA_CLARO)      # hab2
crear_suelo(-3, -2.5, 2, 2, COLOR_MARMOL)            # bano marmol

# Rodapies
for x in [-4.8, -3.8, -2.8, -1.8, -0.8, 0.2, 1.2, 2.2, 3.2, 4.2]:
    for y_rod in [-4.8, -3.8, -2.8, -1.8, -0.8, 0.2, 1.2, 2.2, 3.2, 4.2]:
        crear_caja(x, y_rod, 0.08, 0.04, 0.04, 0.08, (0.95, 0.95, 0.93), nombre=f"Rodapie_{x}_{y_rod}")

# ============================================================
# VENTANALES
# ============================================================
crear_ventanal(0, 5, 2.5, 2.4)
crear_ventanal(2.5, 5, 2.5, 2.4)
crear_ventanal(-1.5, 5, 1.5, 2.4)
crear_ventanal(4.5, -5, 1.5, 1.8)  # ventana hab1
crear_ventanal(4.5, 1, 1.5, 1.8)   # ventana hab2

# Cortinas
for vx in [-1.5, 0, 2.5]:
    crear_caja(vx, 5.05, 2.5, 0.05, 0.02, 2.6, (0.9, 0.88, 0.85), roughness=0.9, nombre=f"Persiana_{vx}")

# ============================================================
# COCINA (integrada en salon)
# ============================================================
crear_caja(-2.5, 1.5, 0.5, 0.6, 3.5, 1.0, (0.4, 0.4, 0.4), roughness=0.3, metallic=0.6, nombre="Encimera")
crear_caja(-2.5, 1.5, 0.85, 0.6, 3.5, 0.05, COLOR_MARMOL, roughness=0.3, nombre="Superficie_cocina")
crear_caja(-2.5, 3.2, 1.2, 0.55, 0.5, 0.8, COLOR_ACERO, metallic=0.9, nombre="Horno")
crear_caja(-2.5, 0.2, 1.2, 0.55, 0.5, 0.8, COLOR_ACERO, metallic=0.9, nombre="Lavavajillas")
crear_caja(-2.5, -0.5, 0.3, 0.6, 0.6, 0.6, (0.9, 0.9, 0.9), roughness=0.3, nombre="Fregadero")
crear_caja(-4.5, 1.5, 0.9, 0.6, 3.5, 1.8, COLOR_BLANCO, roughness=0.7, nombre="Mueble_cocina")

# ============================================================
# SALON-COMEDOR
# ============================================================
# Mesa comedor
crear_caja(0.5, 3, 0.75, 2.0, 1.0, 0.05, COLOR_MADERA, roughness=0.5, nombre="Mesa_tabla")
for (mx, my) in [(0.5-0.9, 3-0.45), (0.5+0.9, 3-0.45), (0.5-0.9, 3+0.45), (0.5+0.9, 3+0.45)]:
    crear_caja(mx, my, 0.35, 0.05, 0.05, 0.7, COLOR_MADERA, roughness=0.5, nombre=f"Pata_mesa")

# Sillas
for i in range(6):
    angulo = i * math.pi / 3
    rad = 1.3
    sx = 0.5 + rad * math.cos(angulo)
    sy = 3 + rad * math.sin(angulo)
    crear_caja(sx, sy, 0.45, 0.45, 0.45, 0.45, COLOR_BLANCO, roughness=0.7, nombre=f"Asiento_{i}")
    crear_caja(sx, sy, 0.9, 0.45, 0.05, 0.45, (0.6, 0.6, 0.6), roughness=0.8, nombre=f"Respaldo_{i}")

# Sofa
crear_caja(-1.5, 5.5, 0.4, 2.8, 0.9, 0.4, (0.55, 0.55, 0.58), roughness=0.9, nombre="Sofa_base")
crear_caja(-1.5, 5.5, 0.75, 2.8, 0.9, 0.3, (0.5, 0.5, 0.55), roughness=0.9, nombre="Sofa_cojin")
crear_caja(-1.5, 6.0, 0.75, 2.8, 0.1, 0.6, (0.5, 0.5, 0.55), roughness=0.9, nombre="Sofa_respaldo")

# Mesa centro
crear_caja(-1.5, 4.5, 0.4, 1.2, 0.7, 0.05, COLOR_MADERA, roughness=0.5, nombre="Mesa_centro")
for (mx, my) in [(-1.5-0.55, 4.5-0.3), (-1.5+0.55, 4.5-0.3), (-1.5-0.55, 4.5+0.3), (-1.5+0.55, 4.5+0.3)]:
    crear_caja(mx, my, 0.18, 0.03, 0.03, 0.36, COLOR_ACERO, metallic=0.8, nombre=f"Pata_mesa_centro")

# Estanteria
crear_caja(-4.5, 4.5, 1.2, 0.3, 1.5, 2.4, COLOR_MADERA, roughness=0.6, nombre="Estanteria")
for i in range(4):
    crear_caja(-4.5, 4.5, 0.3 + i*0.6, 0.25, 1.4, 0.03, COLOR_MADERA_CLARO, roughness=0.5, nombre=f"Estante_{i}")

# Cuadro
crear_caja(-4.5, 2.5, 2.0, 0.02, 1.2, 0.8, (0.2, 0.3, 0.5), roughness=0.5, nombre="Cuadro_abstracto")
crear_caja(-4.5, 2.5, 1.58, 0.025, 1.3, 0.04, COLOR_MADERA, roughness=0.5, nombre="Marco_cuadro")

# ============================================================
# LAMPARAS
# ============================================================
crear_lampara_techo(1, 3.5)
crear_lampara_techo(4.5, -2.5)
crear_lampara_techo(4.5, 1)
crear_lampara_techo(-2.5, 3.5)
crear_lampara_techo(-3, -2.5)

# Lampara colgante sobre mesa
crear_caja(0.5, 3, ALTURA_TECHO - 0.1, 0.02, 0.02, 0.5, COLOR_ACERO, metallic=0.8, nombre="Cable_lampara")
crear_caja(0.5, 3, 2.1, 0.3, 0.3, 0.15, (1.0, 0.95, 0.8), emission=5.0, nombre="Bombilla")

# ============================================================
# HABITACIONES
# ============================================================
# Hab 1 - Cama
crear_caja(4.5, -2.5, 0.4, 1.5, 2.0, 0.4, COLOR_BLANCO, roughness=0.7, nombre="Cama1_base")
crear_caja(4.5, -2.5, 0.7, 1.5, 2.0, 0.2, COLOR_BLANCO, roughness=0.9, nombre="Cama1_colchon")
crear_caja(4.5, -1.6, 0.9, 1.5, 0.6, 0.3, COLOR_BLANCO, roughness=0.9, nombre="Cama1_almohada")
crear_caja(4.5, -3.4, 0.9, 1.5, 0.1, 0.5, (0.3, 0.3, 0.5), roughness=0.9, nombre="Cama1_cabecero")

# Mesita noche
crear_caja(3.7, -2.5, 0.5, 0.4, 0.4, 0.5, COLOR_MADERA, roughness=0.5, nombre="Mesita_noche_1")
crear_caja(5.3, -2.5, 0.5, 0.4, 0.4, 0.5, COLOR_MADERA, roughness=0.5, nombre="Mesita_noche_2")

# Armario hab1
crear_caja(6.5, -2.5, 1.2, 0.5, 2.5, 2.4, COLOR_BLANCO, roughness=0.7, nombre="Armario_1")

# Hab 2 - Cama (similar)
crear_caja(4.5, 1, 0.4, 1.5, 2.0, 0.4, COLOR_BLANCO, roughness=0.7, nombre="Cama2_base")
crear_caja(4.5, 1, 0.7, 1.5, 2.0, 0.2, COLOR_BLANCO, roughness=0.9, nombre="Cama2_colchon")
crear_caja(4.5, 1.9, 0.9, 1.5, 0.6, 0.3, COLOR_BLANCO, roughness=0.9, nombre="Cama2_almohada")
crear_caja(4.5, 0.1, 0.9, 1.5, 0.1, 0.5, (0.5, 0.3, 0.3), roughness=0.9, nombre="Cama2_cabecero")
crear_caja(6.5, 1, 0.5, 0.4, 0.4, 0.5, COLOR_MADERA, roughness=0.5, nombre="Mesita_noche_3")

# Hab 3 - Cama
crear_caja(-2.5, 3.5, 0.4, 1.2, 1.8, 0.4, COLOR_BLANCO, roughness=0.7, nombre="Cama3_base")
crear_caja(-2.5, 3.5, 0.7, 1.2, 1.8, 0.2, COLOR_BLANCO, roughness=0.9, nombre="Cama3_colchon")

# ============================================================
# BANO
# ============================================================
crear_caja(-3, -2.5, 0.4, 0.8, 1.6, 0.4, COLOR_BLANCO, roughness=0.5, nombre="Banera")
crear_caja(-3, -1.2, 0.8, 0.3, 0.3, 0.8, COLOR_BLANCO, roughness=0.5, nombre="Lavabo")
crear_caja(-3, -3.2, 0.8, 0.3, 0.3, 0.8, COLOR_BLANCO, roughness=0.5, nombre="Inodoro")
crear_caja(-3.5, -2.5, 1.8, 0.02, 1.0, 0.6, (0.7, 0.85, 0.9), roughness=0.1, specular=1.0, nombre="Espejo")

# ============================================================
# VEGETACION
# ============================================================
# Maceta salon
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.1, depth=0.2, location=(-2.5, 4.5, 0.2))
maceta = bpy.context.object
maceta.name = "Maceta"
mat_maceta = crear_material("Mat_maceta", (0.3, 0.2, 0.1), roughness=0.8)
if maceta.data.materials:
    maceta.data.materials[0] = mat_maceta

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(-2.5, 4.5, 0.5))
planta = bpy.context.object
planta.name = "Planta"
mat_planta = crear_material("Mat_planta", COLOR_VERDE, roughness=0.9)
if planta.data.materials:
    planta.data.materials[0] = mat_planta

# ============================================================
# ILUMINACION
# ============================================================
# Luz natural desde ventanales
crear_luz_area(0, 6, 3.5, potencia=8000, color=(1.0, 0.92, 0.8), size=4.0)
crear_luz_area(-2, 6, 3, potencia=4000, color=(1.0, 0.92, 0.8), size=3.0)

# Sol
bpy.ops.object.light_add(type='SUN', location=(2, 8, 10))
sol = bpy.context.object
sol.data.energy = 8
sol.data.color = (1.0, 0.88, 0.7)
sol.rotation_euler = (math.radians(50), 0, math.radians(-35))
sol.name = "Sol"

# Luces de ambiente
crear_luz_area(0, 0, 2.5, potencia=200, color=(1.0, 0.95, 0.9), size=5.0)

# ============================================================
# CAMARA
# ============================================================
bpy.ops.object.camera_add(location=(5, -3, 2.0))
cam = bpy.context.object
cam.rotation_euler = (math.radians(50), 0, math.radians(-20))
cam.data.lens = 20
cam.data.sensor_width = 36
bpy.context.scene.camera = cam

# Segunda camara (vista cocina)
bpy.ops.object.camera_add(location=(-3, -1, 1.8))
cam2 = bpy.context.object
cam2.rotation_euler = (math.radians(55), 0, math.radians(30))
cam2.data.lens = 24
cam2.data.sensor_width = 36
cam2.name = "Camara_cocina"

# ============================================================
# RENDER EEVEE 4K
# ============================================================
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.filepath = '/root/piso_sagrada_final.png'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

eevee = scene.eevee
eevee.taa_samples = 64
eevee.taa_render_samples = 128
eevee.use_bloom = True
eevee.bloom_intensity = 0.08
eevee.bloom_radius = 6.5
eevee.use_ssr = True
eevee.ssr_quality = 0.5
eevee.use_gtao = True
eevee.gtao_distance = 0.5
eevee.gtao_factor = 1.0
eevee.shadow_cascade_size = '4096'
eevee.use_soft_shadows = True

scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium Contrast'
scene.view_settings.exposure = 0.15
scene.view_settings.gamma = 1.0

print("=== MODELO COMPLETO ===")
print("Piso 102m2: salon+comedor+cocina, 3 hab, 2 banos")
print("Detalles: cocina equipada, muebles, cortinas, cuadros, plantas, lamparas")
print("Render: /root/piso_sagrada_final.png")

bpy.ops.wm.save_as_mainfile(filepath='/root/piso_sagrada_final.blend')
