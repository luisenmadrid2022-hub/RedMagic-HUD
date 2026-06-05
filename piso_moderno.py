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
# MATERIALES
# ============================================================
def crear_material(nombre, color, roughness=0.5, metallic=0.0, emission=0.0):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = nodes.get('Principled BSDF')
    if principled:
        principled.inputs['Base Color'].default_value = (*color, 1.0)
        principled.inputs['Roughness'].default_value = roughness
        principled.inputs['Metallic'].default_value = metallic
        if emission > 0:
            principled.inputs['Emission Strength'].default_value = emission
            principled.inputs['Emission Color'].default_value = (*color, 1.0)
    return mat

def crear_caja(x, y, z, sx, sy, sz, color, roughness=0.5, metallic=0.0, nombre="Caja", emission=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.object
    obj.scale = (sx/2, sy/2, sz/2)
    obj.name = nombre
    mat = crear_material(f"Mat_{nombre}", color, roughness, metallic, emission)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

# Paleta moderna minimalista
BLANCO_ROTO = (0.96, 0.96, 0.95)
GRIS_SUELO = (0.35, 0.35, 0.37)
GRIS_CLARO = (0.75, 0.75, 0.77)
GRIS_MEDIO = (0.55, 0.55, 0.57)
GRIS_OSCURO = (0.25, 0.25, 0.27)
ACERO = (0.65, 0.65, 0.68)
NEGRO_MATE = (0.1, 0.1, 0.12)
TECHO = (0.98, 0.98, 0.98)
VIDRIO = (0.7, 0.85, 0.95)

# ============================================================
# SUELO Y PAREDES
# ============================================================
# Suelo base
crear_caja(0, 0, -0.05, ANCHO_TOTAL, LARGO_TOTAL, 0.1, GRIS_SUELO, roughness=0.8, nombre="Suelo_base")

# Paredes exteriores
for y in [-5.1, 5.1]:
    crear_caja(0, y, ALTURA_TECHO/2, ANCHO_TOTAL, ALTURA_TECHO, 0.15, BLANCO_ROTO, roughness=0.9, nombre=f"Pared_ext_y{y}")
for x in [-5, 5]:
    crear_caja(x, 0, ALTURA_TECHO/2, 0.15, ALTURA_TECHO, LARGO_TOTAL, BLANCO_ROTO, roughness=0.9, nombre=f"Pared_ext_x{x}")

# Techos
for (cx, cy, cw, cl) in [(1, 3.5, 6, 6), (-2.5, 3.5, 3.5, 4), (4.5, -2.5, 4, 4), (4.5, 1, 4, 3.5), (-3, -2.5, 2, 2)]:
    crear_caja(cx, cy, ALTURA_TECHO, cw, cl, 0.05, TECHO, roughness=0.9, nombre=f"Techo_{cx}")

# Paredes interiores
Pared = lambda x, y, w, h, d: crear_caja(x, y, h/2, w, h, d, BLANCO_ROTO, roughness=0.9, nombre=f"Pared_{x}_{y}")
Pared(-2, -1.5, 0.12, ALTURA_TECHO, 5)
Pared(2.5, -1, 4.5, ALTURA_TECHO, 0.12)
Pared(4.5, -2.5, 0.12, ALTURA_TECHO, 3)
Pared(4.5, 1, 0.12, ALTURA_TECHO, 3)

# Rodapies gris oscuro
for xr in [x*0.5 for x in range(-18, 19)]:
    crear_caja(xr, 0, 0.05, 0.4, 0.04, 0.08, GRIS_OSCURO, nombre=f"Rodapie_{xr}")

# ============================================================
# VENTANALES GRANDES
# ============================================================
for (vx, vw) in [(0, 2.8), (2.5, 2.8), (-1.5, 1.8)]:
    crear_caja(vx, 5.1, ALTURA_TECHO/2, vw, 0.05, 2.4, VIDRIO, roughness=0.0, nombre=f"Ventanal_{vx}")
    crear_caja(vx, 5.1, 0.05, vw+0.2, 0.08, 0.08, GRIS_OSCURO, nombre=f"Alfeizar_{vx}")
    crear_caja(vx, 5.1, 2.65, vw+0.2, 0.08, 0.08, GRIS_OSCURO, nombre=f"Dintel_{vx}")

# ============================================================
# COCINA ABIERTA (gris mate/acero)
# ============================================================
# Encimera
crear_caja(-2.5, 1.5, 0.85, 0.6, 3.5, 1.7, GRIS_OSCURO, roughness=0.7, nombre="Mueble_cocina")
crear_caja(-2.5, 1.5, 0.92, 0.6, 3.5, 0.04, GRIS_CLARO, roughness=0.3, nombre="Encimera")

# Electrodomesticos empotrados gris mate
crear_caja(-2.5, 3.2, 1.2, 0.55, 0.5, 0.85, ACERO, roughness=0.4, metallic=0.5, nombre="Horno")
crear_caja(-2.5, 0.2, 1.2, 0.55, 0.5, 0.85, ACERO, roughness=0.4, metallic=0.5, nombre="Lavavajillas")
crear_caja(-2.5, -0.4, 0.35, 0.5, 0.5, 0.7, NEGRO_MATE, roughness=0.8, nombre="Frigorifico")
crear_caja(-2.5, -0.5, 0.3, 0.6, 0.6, 0.6, ACERO, roughness=0.3, metallic=0.6, nombre="Fregadero")

# Campana extractora
crear_caja(-2.5, 2.2, 2.0, 0.5, 0.3, 0.15, NEGRO_MATE, roughness=0.8, nombre="Campana")

# ============================================================
# SALON-COMEDOR
# ============================================================
# Mesa comedor
crear_caja(0.5, 3, 0.75, 2.0, 1.0, 0.04, GRIS_CLARO, roughness=0.5, nombre="Mesa")
for (mx, my) in [(0.5-0.9, 3-0.45), (0.5+0.9, 3-0.45), (0.5-0.9, 3+0.45), (0.5+0.9, 3+0.45)]:
    crear_caja(mx, my, 0.35, 0.04, 0.04, 0.7, NEGRO_MATE, roughness=0.8, nombre=f"Pata_mesa")

# Sillas
for i in range(6):
    ang = i * math.pi / 3
    sx = 0.5 + 1.3 * math.cos(ang)
    sy = 3 + 1.3 * math.sin(ang)
    crear_caja(sx, sy, 0.45, 0.4, 0.4, 0.45, NEGRO_MATE, roughness=0.8, nombre=f"Asiento_{i}")
    crear_caja(sx, sy, 0.85, 0.4, 0.04, 0.4, GRIS_MEDIO, roughness=0.7, nombre=f"Respaldo_{i}")

# Sofa modular gris
crear_caja(-1.5, 5.5, 0.4, 2.8, 0.9, 0.4, GRIS_MEDIO, roughness=0.9, nombre="Sofa_base")
crear_caja(-1.5, 5.5, 0.75, 2.8, 0.9, 0.3, GRIS_CLARO, roughness=0.9, nombre="Sofa_cojin")
crear_caja(-1.5, 6.0, 0.75, 2.8, 0.1, 0.6, GRIS_MEDIO, roughness=0.9, nombre="Sofa_respaldo")

# Mesa centro baja
crear_caja(-1.5, 4.5, 0.35, 1.2, 0.7, 0.04, GRIS_OSCURO, roughness=0.6, nombre="Mesa_centro")

# Estanteria abierta
crear_caja(-4.5, 4.5, 1.5, 0.3, 1.8, 3.0, GRIS_OSCURO, roughness=0.7, nombre="Estanteria")
for i in range(5):
    crear_caja(-4.5, 4.5, 0.3 + i*0.6, 0.25, 1.7, 0.03, GRIS_CLARO, roughness=0.5, nombre=f"Estante_{i}")

# ============================================================
# LAMPARAS
# ============================================================
crear_caja(0.5, 3, ALTURA_TECHO-0.1, 0.02, 0.02, 0.5, NEGRO_MATE, roughness=0.8, nombre="Cable_lampara")
crear_caja(0.5, 3, 2.1, 0.25, 0.25, 0.12, (1.0, 0.95, 0.85), emission=3.0, nombre="Bombilla")

for (lx, ly) in [(1, 3.5), (4.5, -2.5), (4.5, 1), (-2.5, 3.5), (-3, -2.5)]:
    crear_caja(lx, ly, ALTURA_TECHO-0.02, 0.2, 0.2, 0.04, GRIS_OSCURO, metallic=0.8, nombre=f"Base_luz_{lx}")

# ============================================================
# HABITACIONES
# ============================================================
# Hab 1
crear_caja(4.5, -2.5, 0.35, 1.5, 1.8, 0.35, BLANCO_ROTO, roughness=0.8, nombre="Cama1_base")
crear_caja(4.5, -2.5, 0.65, 1.5, 1.8, 0.25, GRIS_CLARO, roughness=0.9, nombre="Cama1_colchon")
crear_caja(4.5, -3.4, 0.85, 1.5, 0.1, 0.5, GRIS_MEDIO, roughness=0.9, nombre="Cama1_cabecero")
crear_caja(3.7, -2.5, 0.5, 0.4, 0.4, 0.5, GRIS_OSCURO, roughness=0.7, nombre="Mesita1")

# Hab 2
crear_caja(4.5, 1, 0.35, 1.5, 1.8, 0.35, BLANCO_ROTO, roughness=0.8, nombre="Cama2_base")
crear_caja(4.5, 1, 0.65, 1.5, 1.8, 0.25, GRIS_CLARO, roughness=0.9, nombre="Cama2_colchon")
crear_caja(4.5, 0.1, 0.85, 1.5, 0.1, 0.5, GRIS_MEDIO, roughness=0.9, nombre="Cama2_cabecero")

# Hab 3
crear_caja(-2.5, 3.5, 0.35, 1.3, 1.8, 0.35, BLANCO_ROTO, roughness=0.8, nombre="Cama3_base")
crear_caja(-2.5, 3.5, 0.65, 1.3, 1.8, 0.25, GRIS_CLARO, roughness=0.9, nombre="Cama3_colchon")

# ============================================================
# BANO
# ============================================================
crear_caja(-3, -0.8, 0.4, 0.8, 0.4, 0.4, BLANCO_ROTO, roughness=0.5, nombre="Lavabo")
crear_caja(-3, -3.2, 0.4, 0.4, 0.4, 0.4, BLANCO_ROTO, roughness=0.5, nombre="Inodoro")
crear_caja(-3.5, -2.5, 1.8, 0.02, 1.0, 0.6, (0.75, 0.85, 0.9), roughness=0.1, nombre="Espejo")

# ============================================================
# ILUMINACION
# ============================================================
crear_caja(0, 6, 3.5, 4.0, 0.1, 0.05, (1.0, 0.92, 0.8), emission=8.0, nombre="Luz_ventanal")

bpy.ops.object.light_add(type='SUN', location=(2, 8, 10))
sol = bpy.context.object
sol.data.energy = 10
sol.data.color = (1.0, 0.9, 0.75)
sol.rotation_euler = (math.radians(45), 0, math.radians(-30))
sol.name = "Sol"

# ============================================================
# CAMARA GRAN ANGULAR
# ============================================================
bpy.ops.object.camera_add(location=(5, -4, 2.0))
cam = bpy.context.object
cam.rotation_euler = (math.radians(55), 0, math.radians(-22))
cam.data.lens = 18
cam.data.sensor_width = 36
bpy.context.scene.camera = cam

# ============================================================
# RENDER EEVEE
# ============================================================
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.filepath = '/root/piso_moderno.png'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

eevee = scene.eevee
eevee.taa_samples = 64
eevee.taa_render_samples = 128
eevee.use_bloom = True
eevee.bloom_intensity = 0.05
eevee.use_ssr = True
eevee.use_gtao = True
eevee.use_soft_shadows = True
eevee.shadow_cascade_size = '4096'

scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium Contrast'
scene.view_settings.exposure = 0.2

print("=== MODELO CREADO ===")
print("Piso 102m2 - Estilo minimalista grises")
print("Cocina abierta, 3 dorm, 2 banos")
print("Iluminacion natural intensa")
print("Render en /root/piso_moderno.png")

bpy.ops.wm.save_as_mainfile(filepath='/root/piso_moderno.blend')
