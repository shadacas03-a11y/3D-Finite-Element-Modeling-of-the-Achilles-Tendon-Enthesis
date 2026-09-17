from abaqus import *
from abaqusConstants import *
import regionToolset

MODEL = 'FInalModel'

model = mdb.models[MODEL]
a = model.rootAssembly

# -------------------------------------------------------
# STEP
# -------------------------------------------------------
if 'LOADING' in model.steps.keys():
    del model.steps['LOADING']

model.StaticStep(
    name='LOADING',
    previous='Initial',
    nlgeom=ON, 
    initialInc=0.01,
    minInc=1e-8,
    maxInc=0.05,
    maxNumInc=500
)

print('Static step created.')

# -------------------------------------------------------
# REGIONS
# -------------------------------------------------------
rpRegion = a.sets['RP_PROXIMAL']
distalRegion = a.sets['DISTAL_FIXED_ASM']

# -------------------------------------------------------
# DISTAL FIXED (Base anclada)
# -------------------------------------------------------
if 'BC_Distal' in model.boundaryConditions.keys():
    del model.boundaryConditions['BC_Distal']

model.DisplacementBC(
    name='BC_Distal',
    createStepName='Initial',
    region=distalRegion,
    u1=0.0,
    u2=0.0,
    u3=0.0,
    ur1=UNSET,
    ur2=UNSET,
    ur3=UNSET
)

print('Distal BC created.')

# -------------------------------------------------------
# RP TRANSVERSE CONSTRAINT 
# -------------------------------------------------------
if 'BC_RP' in model.boundaryConditions.keys():
    del model.boundaryConditions['BC_RP']

model.DisplacementBC(
    name='BC_RP',
    createStepName='Initial',
    region=rpRegion,
    u1=0.0,   # Bloquea movimiento lateral en X
    u2=0.0,   # Bloquea movimiento lateral en Y
    u3=UNSET, # Deja libre el eje Z para jalar
    ur1=UNSET,
    ur2=UNSET,
    ur3=UNSET
)

print('RP BC created.')

# -------------------------------------------------------
# FORCE (1256 N jalando en el eje Z)
# -------------------------------------------------------
if 'LOAD_RP' in model.loads.keys():
    del model.loads['LOAD_RP']

model.ConcentratedForce(
    name='LOAD_RP',
    createStepName='LOADING',
    region=rpRegion,
    cf1=0.0,
    cf2=0.0,
    cf3=1256.0 
)

print('Load created.')

# -------------------------------------------------------
# FIELD OUTPUT
# -------------------------------------------------------
model.fieldOutputRequests['F-Output-1'].setValues(
    variables=(
        'S',
        'LE',
        'U',
        'RF',
        'E'
    )
)

print('Field output modified.')

# -------------------------------------------------------
# HISTORY OUTPUT (Guardar datos de Z para graficar)
# -------------------------------------------------------
if 'H-RP' in model.historyOutputRequests.keys():
    del model.historyOutputRequests['H-RP']

model.HistoryOutputRequest(
    name='H-RP',
    createStepName='LOADING',
    variables=('U3','RF3'), 
    region=rpRegion
)

print('History output created.')

# -------------------------------------------------------
# JOB
# -------------------------------------------------------
JOB = 'Job_3Part_Enthesis'

if JOB in mdb.jobs.keys():
    del mdb.jobs[JOB]

mdb.Job(
    name=JOB,
    model=MODEL,
    type=ANALYSIS,
    numCpus=4,
    numDomains=4,
    multiprocessingMode=DEFAULT,
    memory=90,
    memoryUnits=PERCENTAGE
)

print('--------------------------------')
print('SCRIPT 07 FINISHED SUCCESSFULLY')
print('JOB CREATED: Job_3Part_Enthesis')
print('READY TO RUN')
print('--------------------------------')
