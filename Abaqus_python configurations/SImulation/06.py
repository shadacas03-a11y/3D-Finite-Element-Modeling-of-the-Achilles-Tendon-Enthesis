from abaqus import *
from abaqusConstants import *
import regionToolset

MODEL = 'FInalModel'
PART = 'PART-1'

model = mdb.models[MODEL]
a = model.rootAssembly

# -------------------------------------------------------
# Instance
# -------------------------------------------------------
inst = a.instances['PART-1-1']

# -------------------------------------------------------
# Create RP from proximal nodes
# -------------------------------------------------------
nodes = inst.sets['PROXIMAL_LOAD'].nodes

x = y = z = 0.0

for n in nodes:
    x += n.coordinates[0]
    y += n.coordinates[1]
    z += n.coordinates[2]

N = float(len(nodes))

rpFeature = a.ReferencePoint(
    point=(x/N, y/N, z/N)
)

rp = a.referencePoints[rpFeature.id]

if 'RP_PROXIMAL' in a.sets.keys():
    del a.sets['RP_PROXIMAL']

a.Set(
    name='RP_PROXIMAL',
    referencePoints=(rp,)
)

print('Reference Point created.')

# -------------------------------------------------------
# Region made ONLY from nodes
# -------------------------------------------------------
proxRegion = regionToolset.Region(
    nodes=inst.sets['PROXIMAL_LOAD'].nodes
)

rpRegion = a.sets['RP_PROXIMAL']

# -------------------------------------------------------
# Delete old coupling if exists
# -------------------------------------------------------
if 'PROXIMAL_COUPLING' in model.constraints.keys():
    del model.constraints['PROXIMAL_COUPLING']

# -------------------------------------------------------
# Coupling
# -------------------------------------------------------
model.Coupling(
    name='PROXIMAL_COUPLING',
    controlPoint=rpRegion,
    surface=proxRegion,
    influenceRadius=WHOLE_SURFACE,
    couplingType=DISTRIBUTING,
    weightingMethod=UNIFORM,
    localCsys=None,
    u1=ON,
    u2=ON,
    u3=ON,
    ur1=OFF,
    ur2=OFF,
    ur3=OFF
)

print('--------------------------------')
print('SCRIPT 06 FINISHED SUCCESSFULLY')
print('Coupling created without Surface errors.')
print('--------------------------------')
