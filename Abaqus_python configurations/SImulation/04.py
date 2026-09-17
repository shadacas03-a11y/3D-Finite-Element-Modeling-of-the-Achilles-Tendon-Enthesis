from abaqus import *
from abaqusConstants import *

MODEL = 'FInalModel'
model = mdb.models[MODEL]

part_names = ['PART-1', 'PART-1_1', 'PART-1_2']
ORI = 'ORI_TENDON'

for PART in part_names:
    p = model.parts[PART]
    
    # -------------------------------------------------
    # 1. Delete previous material orientation assignments
    # -------------------------------------------------
    while len(p.materialOrientations) > 0:
        del p.materialOrientations[0]
        
    # -------------------------------------------------
    # 2. Delete previous datum (Integrated from your script)
    # -------------------------------------------------
    if ORI in p.features.keys():
        del p.features[ORI]
        
    # -------------------------------------------------
    # 3. Create Cartesian datum
    # -------------------------------------------------
    datum_feature = p.DatumCsysByThreePoints(
        name=ORI,
        coordSysType=CARTESIAN,
        origin=(0.0,0.0,0.0),
        point1=(0.0,0.0,1.0),
        point2=(0.0,1.0,0.0)
    )
    
    datum_obj = p.datums[datum_feature.id]
    
    # -------------------------------------------------
    # 4. Assign Orientation to ALL_ELEMENTS
    # -------------------------------------------------
    region = p.sets['ALL_ELEMENTS']
    
    p.MaterialOrientation(
        region=region,
        orientationType=SYSTEM,
        axis=AXIS_1,
        localCsys=datum_obj,
        fieldName='',
        additionalRotationType=ROTATION_NONE,
        angle=0.0,
        additionalRotationField=''
    )
    
    print('Orientation created and assigned to:', PART)

print('--------------------------------')
print('SCRIPT 04 FINISHED SUCCESSFULLY')
print('--------------------------------')
