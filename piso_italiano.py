import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Dimensiones
ANCHO_TOTAL = 10.0
LARGO_TOTAL = 10.2
ALTURA_TECHO = 2.8

# ============================================================
# MATERIALES
# ============================================================
def crear_material(nombre, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    principled = nodes.get('Principled BSDF')
    if principled:
        principled.inputs['Base Color'].default_value = (*color, 1.0)
        principled.inputs['Roughness'].default_value = roughness
        principled.inputs['Metallic'].default_value = metallic
    return mat

def crear_caja(x, y, z, sx, sy, sz, color, roughness=0.5, metallic=0.0, n="Caja"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.object
    obj.scale = (sx/2, sy/2, sz/2)
    obj.name = nombre
    mat = crear_material(f"Mat_{nombre}", color, roughness, metallic)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

P = lambda x,y,z,sx,sy,sz,c,r=0.5,m=0,n="C": crear_caja(x,y,z,sx,sy,sz,c,r,m,n)

# Paleta
BLANCO = (0.96, 0.96, 0.95)
GRIS_SUELO = (0.32, 0.33, 0.35)
GRIS_CLARO = (0.72, 0.73, 0.75)
GRIS_MEDIO = (0.52, 0.53, 0.55)
GRIS_OSCURO = (0.22, 0.23, 0.25)
ACERO = (0.62, 0.63, 0.65)
NEGRO = (0.08, 0.09, 0.10)
TECHO = (0.98, 0.98, 0.98)
MARMOL = (0.88, 0.87, 0.85)

# ============================================================
# SUELO Y PAREDES
# ============================================================
def P(x, y, z, sx, sy, sz, c, r=0.5, m=0, n="C"):
    return crear_caja(x, y, z, sx, sy, sz, c, r, m, n)

S = lambda x,y,z,sx,sz,c,r=0.5: crear_caja(x,y,z,sx,0.1,sz,c,r, n="Suelo")

# Suelo global
S(0, 0, -0.05, ANCHO_TOTAL, LARGO_TOTAL, GRIS_SUELO, 0.8)

for y in [-5.1, 5.1]:
    P(0, y, ALTURA_TECHO/2, ANCHO_TOTAL, ALTURA_TECHO, 0.15, BLANCO, 0.9, n=f"Pared_y{y}")
for x in [-5, 5]:
    P(x, 0, ALTURA_TECHO/2, 0.15, ALTURA_TECHO, LARGO_TOTAL, BLANCO, 0.9, n=f"Pared_x{x}")

for (cx, cy, cw, cl) in [(1, 3.5, 6, 6), (-2.5, 3.5, 3.5, 4), (4.5, -2.5, 4, 4), (4.5, 1, 4, 3.5), (-3, -2.5, 2, 2)]:
    P(cx, cy, ALTURA_TECHO, cw, cl, 0.05, TECHO, 0.9, n=f"Techo_{cx}")

# Paredes interiores
P(-2, -1.5, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 5, BLANCO, 0.9, n="Pared_salon")
P(2.5, -1, 4.5, ALTURA_TECHO, 0.12, BLANCO, 0.9, n="Pared_pasillo")
P(4.5, -2.5, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 3, BLANCO, 0.9, n="Pared_h1h2")
P(4.5, 1, ALTURA_TECHO/2, 0.12, ALTURA_TECHO, 3, BLANCO, 0.9, n="Pared_h2b")

# ============================================================
# VENTANALES SUELO A TECHO
# ============================================================
for (vx, vw) in [(0, 3.0), (2.5, 2.5), (-1.5, 2.0)]:
    P(vx, 5.1, ALTURA_TECHO/2, vw, 0.05, 2.6, (0.6, 0.8, 0.95), 0.0, n=f"Vidrio_{vx}")
    P(vx, 5.1, 0.05, vw+0.3, 0.08, 0.08, GRIS_OSCURO, 0.5, n=f"Marco_bajo_{vx}")
    P(vx, 5.1, 2.7, vw+0.3, 0.08, 0.08, GRIS_OSCURO, 0.5, n=f"Marco_alto_{vx}")
    P(vx-0.15, 5.1, 1.3, 0.04, 0.05, 2.6, GRIS_OSCURO, 0.5, n=f"Jamba_{vx}")

# Ventana cocina (oscilobatiente)
P(-2.5, 5.1, 1.3, 1.2, 0.05, 1.6, (0.65, 0.82, 0.92), 0.0, n="Ventana_cocina")
P(-2.5, 5.1, 2.2, 1.3, 0.06, 0.06, GRIS_MEDIO, 0.4, n="Marco_cocina")

# ============================================================
# COCINA LINEAL ITALIANA (gola, sin tiradores)
# ============================================================
# Muebles altos blancos mate
P(-4.5, 1.5, 1.8, 0.5, 3.5, 3.6, BLANCO, 0.7, n="Mueble_alto")
# Muebles bajos
P(-4.5, 1.5, 0.45, 0.5, 3.5, 0.9, BLANCO, 0.7, n="Mueble_bajo")
# Encimera cuarzo gris claro
P(-4.5, 1.5, 0.92, 0.55, 3.5, 0.04, MARMOL, 0.2, n="Encimera_cuarzo")
# Salpicadero
P(-4.5, 3.2, 1.5, 0.02, 0.5, 1.2, MARMOL, 0.2, n="Salpicadero")

# Nevera panelada oculta
P(-4.5, -0.3, 0.9, 0.5, 0.7, 1.8, BLANCO, 0.7, n="Nevera")

# Horno + microondas columna acero
P(-4.5, 3.2, 1.3, 0.5, 0.5, 0.9, ACERO, 0.3, 0.6, n="Horno")
P(-4.5, 3.2, 2.2, 0.5, 0.5, 0.5, ACERO, 0.3, 0.6, n="Microondas")

# Placa induccion negra
P(-4.5, 1.0, 0.93, 0.5, 0.6, 0.02, NEGRO, 0.5, n="Placa_induccion")

# ============================================================
# SALON-COMEDOR
# ============================================================
# Mesa comedor lacada blanca + patas metal gris
P(0.5, 3, 0.75, 1.8, 0.9, 0.04, BLANCO, 0.3, n="Mesa")
for (mx, my) in [(0.5-0.8, 3-0.4), (0.5+0.8, 3-0.4), (0.5-0.8, 3+0.4), (0.5+0.8, 3+0.4)]:
    P(mx, my, 0.35, 0.04, 0.04, 0.7, GRIS_MEDIO, 0.4, 0.7, n=f"Pata_mesa")

# Sillas diseño
for i in range(4):
    ang = i * math.pi / 2
    sx = 0.5 + 1.2 * math.cos(ang)
    sy = 3 + 1.2 * math.sin(ang)
    P(sx, sy, 0.45, 0.4, 0.4, 0.45, GRIS_OSCURO, 0.8, n=f"Silla_base_{i}")
    P(sx, sy, 0.85, 0.4, 0.04, 0.4, GRIS_CLARO, 0.8, n=f"Silla_resp_{i}")

# Sofa modular tela gris claro
P(-1.5, 5.5, 0.4, 2.6, 0.9, 0.4, GRIS_CLARO, 0.9, n="Sofa_base")
P(-1.5, 5.5, 0.75, 2.6, 0.9, 0.3, BLANCO, 0.9, n="Sofa_cojin")
P(-1.5, 6.0, 0.75, 2.6, 0.1, 0.6, GRIS_CLARO, 0.9, n="Sofa_respaldo")

# Mesa centro minimalista
P(-1.5, 4.5, 0.35, 1.0, 0.6, 0.04, NEGRO, 0.6, n="Mesa_centro")

# TV empotrada en pared panelada
P(-4.5, 2.5, 1.5, 0.02, 1.5, 0.8, (0.05, 0.05, 0.08), 0.3, n="TV")
P(-4.5, 2.5, 1.5, 0.03, 1.6, 0.9, BLANCO, 0.9, n="Panel_TV")

# ============================================================
# ILUMINACION ARQUITECTONICA
# ============================================================
# Foseados LED (tiras ocultas en techo)
for (lx, ly, lw, ll) in [(1, 3.5, 5, 5), (-1.5, 5.5, 2, 1.5), (0.5, 3, 1.5, 0.8)]:
    P(lx, ly, ALTURA_TECHO-0.05, lw, ll, 0.02, (1.0, 0.95, 0.85), 0.0, emission=2.0, n=f"LED_foseado_{lx}")

# Spots empotrados
for (sx, sy) in [(0, 3.5), (1.5, 3), (-1, 5), (4.5, -2.5), (4.5, 1), (-2.5, 3.5), (-3, -2.5)]:
    P(sx, sy, ALTURA_TECHO-0.02, 0.08, 0.08, 0.04, (1.0, 0.95, 0.85), 0.0, emission=1.0, n=f"Spot_{sx}")

# Lampada colgante sobre mesa
P(0.5, 3, ALTURA_TECHO-0.1, 0.015, 0.015, 0.4, NEGRO, 0.8, n="Cable_luz")
P(0.5, 3, 2.15, 0.15, 0.15, 0.1, (1.0, 0.92, 0.8), 0.0, emission=5.0, n="Bombilla")

# Luz natural intensa (sol)
P(0, 6, 3.5, 4.0, 0.1, 0.02, (1.0, 0.92, 0.8), 0.0, emission=12.0, n="Luz_ventanal")

bpy.ops.object.light_add(type='SUN', location=(2, 8, 10))
sol = bpy.context.object
sol.data.energy = 15
sol.data.color = (1.0, 0.9, 0.75)
sol.rotation_euler = (math.radians(40), 0, math.radians(-25))
sol.name = "Sol_Barcelona"

# ============================================================
# DORMITORIOS (puertas block blanco hasta techo)
# ============================================================
# Puertas
for (px, py) in [(-2, -1.5), (2.5, -2.5), (2.5, 0.5)]:
    P(px, py, 1.2, 0.02, 0.9, 2.4, BLANCO, 0.7, n=f"Puerta_{px}")

# Camas
P(4.5, -2.5, 0.35, 1.4, 1.8, 0.35, BLANCO, 0.8, n="C1_base")
P(4.5, -2.5, 0.65, 1.4, 1.8, 0.25, GRIS_CLARO, 0.9, n="C1_colchon")
P(4.5, -3.4, 0.85, 1.4, 0.1, 0.5, GRIS_MEDIO, 0.9, n="C1_cabecero")
P(3.7, -2.5, 0.5, 0.35, 0.35, 0.5, GRIS_OSCURO, 0.7, n="Mesita1")

P(4.5, 1, 0.35, 1.4, 1.8, 0.35, BLANCO, 0.8, n="C2_base")
P(4.5, 1, 0.65, 1.4, 1.8, 0.25, GRIS_CLARO, 0.9, n="C2_colchon")
P(4.5, 0.1, 0.85, 1.4, 0.1, 0.5, GRIS_MEDIO, 0.9, n="C2_cabecero")

P(-2.5, 3.5, 0.35, 1.2, 1.8, 0.35, BLANCO, 0.8, n="C3_base")
P(-2.5, 3.5, 0.65, 1.2, 1.8, 0.25, GRIS_CLARO, 0.9, n="C3_colchon")

# ============================================================
# BANOS (ducha a ras, mampara, griferia negra)
# ============================================================
# Plato ducha
P(-3, -3.2, 0.02, 0.8, 0.8, 0.04, GRIS_OSCURO, 0.3, n="Plato_ducha")
# Mampara vidrio
P(-3.4, -3.2, 0.6, 0.02, 0.8, 1.2, (0.65, 0.82, 0.92), 0.0, n="Mampara")
# Lavabo
P(-3, -1.2, 0.5, 0.7, 0.35, 0.5, BLANCO, 0.3, n="Lavabo")
# Inodoro
P(-3, -2.0, 0.4, 0.3, 0.3, 0.4, BLANCO, 0.3, n="Inodoro")
# Espejo
P(-3.5, -1.2, 1.2, 0.02, 0.6, 0.4, (0.7, 0.82, 0.9), 0.0, n="Espejo")

# ============================================================
# CAMARA
# ============================================================
bpy.ops.object.camera_add(location=(5.5, -3.5, 2.2))
cam = bpy.context.object
cam.rotation_euler = (math.radians(52), 0, math.radians(-20))
cam.data.lens = 16
cam.data.sensor_width = 36
bpy.context.scene.camera = cam

# ============================================================
# RENDER CONFIG (EEVEE maximizado)
# ============================================================
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160
scene.render.filepath = '/root/piso_italiano.png'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'

eevee = scene.eevee
eevee.taa_samples = 64
eevee.taa_render_samples = 128
eevee.use_bloom = True
eevee.bloom_intensity = 0.04
eevee.bloom_radius = 7.0
eevee.use_ssr = True
eevee.ssr_quality = 0.5
eevee.use_gtao = True
eevee.gtao_distance = 0.5
eevee.gtao_factor = 1.0
eevee.use_soft_shadows = True
eevee.shadow_cascade_size = '4096'

scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'High Contrast'
scene.view_settings.exposure = 0.15
scene.view_settings.gamma = 1.1

print("=== PISO DISENO ITALIANO COMPLETO ===")
print("Cocina gola blanca mate, encimera cuarzo")
print("Ventanal cocina oscilobatiente")
print("Salon-comedor con mesa lacada + sofar modular")
print("TV empotrada en panel, LED en foseados")
print("3 dormitorios con puertas block hasta techo")
print("2 banos con ducha a ras y mampara")
print("Iluminacion natural intensa (sol Barcelona)")
print("Render 4K EEVEE cinematico")
print("")

bpy.ops.wm.save_as_mainfile(filepath='/root/piso_italiano.blend')
