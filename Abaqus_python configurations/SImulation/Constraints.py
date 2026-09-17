from abaqus import *
from abaqusConstants import *

model = mdb.models['FInalModel']
a = model.rootAssembly

# 1. Tie Tendon to UFc
model.Tie(name='TIE_TENDON_UFC', 
          main=a.surfaces['Surf_Tendon'], 
          secondary=a.surfaces['Surf_UFc_Top'], 
          positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

# 2. Tie UFc to CFc
model.Tie(name='TIE_UFC_CFC', 
          main=a.surfaces['Surf_UFc_Bottom'], 
          secondary=a.surfaces['Surf_CFc'], 
          positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

print('Ties successfully created! Assembly is completely unified.')
