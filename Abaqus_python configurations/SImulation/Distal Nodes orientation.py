from abaqus import *
from abaqusConstants import *
import math

MODEL = 'FInalModel'
model = mdb.models[MODEL]
a = model.rootAssembly

# -------------------------------------------------------
# 1. Get Nodes from Assembly Sets
# -------------------------------------------------------
distal_nodes = a.sets['DISTAL_FIXED_ASM'].nodes
proximal_nodes = a.sets['PROXIMAL_LOAD_ASM'].nodes

# -------------------------------------------------------
# 2. Calculate Centroids
# -------------------------------------------------------
xd = yd = zd = 0.0
for n in distal_nodes:
    xd += n.coordinates[0]
    yd += n.coordinates[1]
    zd += n.coordinates[2]
Nd = float(len(distal_nodes))
Cd = (xd/Nd, yd/Nd, zd/Nd)

xp = yp = zp = 0.0
for n in proximal_nodes:
    xp += n.coordinates[0]
    yp += n.coordinates[1]
    zp += n.coordinates[2]
Np = float(len(proximal_nodes))
Cp = (xp/Np, yp/Np, zp/Np)

# -------------------------------------------------------
# 3. Calculate Anatomical Unit Vector
# -------------------------------------------------------
Vx = Cp[0] - Cd[0]
Vy = Cp[1] - Cd[1]
Vz = Cp[2] - Cd[2]
Mag = math.sqrt(Vx**2 + Vy**2 + Vz**2)

ux = Vx / Mag
uy = Vy / Mag
uz = Vz / Mag

# -------------------------------------------------------
# 4. Apply 1256 N Force along the vector
# -------------------------------------------------------
FORCE = 1256.0
cf1_val = FORCE * ux
cf2_val = FORCE * uy
cf3_val = FORCE * uz

model.loads['LOAD_RP'].setValues(cf1=cf1_val, cf2=cf2_val, cf3=cf3_val)

# -------------------------------------------------------
# 5. Free transverse BCs to allow natural stretching
# -------------------------------------------------------
model.boundaryConditions['BC_RP'].setValues(u1=UNSET, u2=UNSET, u3=UNSET)

print('--------------------------------')
print('Anatomical vector calculated!')
print('Force updated to: X=%.1f, Y=%.1f, Z=%.1f' % (cf1_val, cf2_val, cf3_val))
print('--------------------------------')
