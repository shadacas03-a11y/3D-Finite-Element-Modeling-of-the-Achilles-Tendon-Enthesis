from abaqus import *
from abaqusConstants import *
import regionToolset

# =====================================================
# MODEL & PART NAMES 
# =====================================================
MODEL_NAME = 'FInalModel' 

model = mdb.models[MODEL_NAME]

# Nombres por defecto al importar en Centrale
TENDON_NAME = 'PART-1'
UFC_NAME = 'PART-1_1'
CFC_NAME = 'PART-1_2'

p_tendon = model.parts[TENDON_NAME]
p_ufc = model.parts[UFC_NAME]
p_cfc = model.parts[CFC_NAME]

a = model.rootAssembly

# -----------------------------------------------------
# Create Instances
# -----------------------------------------------------
instances = {}

for p_name in [TENDON_NAME, UFC_NAME, CFC_NAME]:
    inst_name = p_name + '-1'
    if inst_name not in a.instances.keys():
        a.Instance(name=inst_name, part=model.parts[p_name], dependent=ON)
    instances[p_name] = a.instances[inst_name]

print('Model :', MODEL_NAME)
print('All 3 instances loaded successfully.')

# =====================================================
# CREATE DISTAL / PROXIMAL NODE SETS 
# =====================================================

# 1. Encontrar el Z-min global (fondo del hueso CFC) 
#    y Z-max global (tope del Tendón)
zmin_global = min(n.coordinates[2] for n in p_cfc.nodes)
zmax_global = max(n.coordinates[2] for n in p_tendon.nodes)

# 2. Calcular la longitud total y el 3% de tolerancia
length = zmax_global - zmin_global
tol = 0.03 * length

print("Total Assembly Length =", length)
print("Tolerance (3%) =", tol)

# 3. Seleccionar Nodos Distales (Fondo del CFC)
distal_nodes = p_cfc.nodes.getByBoundingBox(
    xMin=-1e20, xMax= 1e20,
    yMin=-1e20, yMax= 1e20,
    zMin=zmin_global - 1.0,  # Pequeño margen extra por debajo
    zMax=zmin_global + tol
)

# 4. Seleccionar Nodos Proximales 
proximal_nodes = p_tendon.nodes.getByBoundingBox(
    xMin=-1e20, xMax= 1e20,
    yMin=-1e20, yMax= 1e20,
    zMin=zmax_global - tol,
    zMax=zmax_global + 1.0   # Pequeño margen extra por encima
)

print('Distal nodes (CFC)    :', len(distal_nodes))
print('Proximal nodes (TENDON):', len(proximal_nodes))

# =====================================================
# DELETE OLD SETS (Cleanup)
# =====================================================
if 'DISTAL_FIXED' in p_cfc.sets.keys(): del p_cfc.sets['DISTAL_FIXED']
if 'PROXIMAL_LOAD' in p_tendon.sets.keys(): del p_tendon.sets['PROXIMAL_LOAD']

for s in ['DISTAL_FIXED_ASM', 'PROXIMAL_LOAD_ASM']:
    if s in a.sets.keys():
        del a.sets[s]

# =====================================================
# CREATE PART SETS
# =====================================================
p_cfc.Set(name='DISTAL_FIXED', nodes=distal_nodes)
p_tendon.Set(name='PROXIMAL_LOAD', nodes=proximal_nodes)

print('Part sets created.')

# =====================================================
# CREATE ASSEMBLY SETS
# =====================================================
distal_labels = tuple([n.label for n in distal_nodes])
proximal_labels = tuple([n.label for n in proximal_nodes])

a.Set(
    name='DISTAL_FIXED_ASM',
    nodes=instances[CFC_NAME].nodes.sequenceFromLabels(distal_labels)
)

a.Set(
    name='PROXIMAL_LOAD_ASM',
    nodes=instances[TENDON_NAME].nodes.sequenceFromLabels(proximal_labels)
)

print('Assembly sets created.')

# =====================================================
# SAVE
# =====================================================
print('=====================================')
print('SCRIPT 01 FINISHED: 3-PART ROBUST SETS READY')
print('=====================================')
