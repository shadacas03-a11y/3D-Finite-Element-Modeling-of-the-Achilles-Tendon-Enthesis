from abaqus import *
from abaqusConstants import *
import regionToolset

# =====================================================
# MODEL & PART NAMES 
# =====================================================
MODEL_NAME = 'FInalModel'

model = mdb.models[MODEL_NAME]

TENDON_NAME = 'PART-1'
UFC_NAME = 'PART-1_1'
CFC_NAME = 'PART-1_2'

p_tendon = model.parts[TENDON_NAME]
p_ufc = model.parts[UFC_NAME]
p_cfc = model.parts[CFC_NAME]

# =====================================================
# 1. CREATE MATERIALS
# =====================================================

# --- A. TENDON MATERIAL (HGO) ---
mat_tendon_name = 'TENDON_HGO'
if mat_tendon_name in model.materials.keys():
    del model.materials[mat_tendon_name]
    
mat_tendon = model.Material(name=mat_tendon_name)
mat_tendon.Density(table=((1.0e-9,),))
mat_tendon.Hyperelastic(
    materialType=ANISOTROPIC,
    anisotropicType=HOLZAPFEL,
    behaviorType=COMPRESSIBLE,
    localDirections=1,
    table=((30.549, 0.0, 327.345, 0.01, 0.139),)
)

# --- B. UFC MATERIAL (Placeholder Fix) ---
mat_ufc_name = 'UFC_MATERIAL'
if mat_ufc_name in model.materials.keys():
    del model.materials[mat_ufc_name]
    
mat_ufc = model.Material(name=mat_ufc_name)
mat_ufc.Density(table=((1.0e-9,),))
mat_ufc.Elastic(table=((100.0, 0.45),)) # Changed to standard Elastic to prevent NameError

# --- C. CFC MATERIAL (Placeholder) ---
mat_cfc_name = 'CFC_BONE_MATERIAL'
if mat_cfc_name in model.materials.keys():
    del model.materials[mat_cfc_name]
    
mat_cfc = model.Material(name=mat_cfc_name)
mat_cfc.Density(table=((2.0e-9,),))
mat_cfc.Elastic(table=((1000.0, 0.3),))

print('All 3 Materials created successfully.')

# =====================================================
# 2. CREATE SECTIONS
# =====================================================

if 'Sec_Tendon' in model.sections.keys(): del model.sections['Sec_Tendon']
model.HomogeneousSolidSection(name='Sec_Tendon', material=mat_tendon_name, thickness=None)

if 'Sec_UFC' in model.sections.keys(): del model.sections['Sec_UFC']
model.HomogeneousSolidSection(name='Sec_UFC', material=mat_ufc_name, thickness=None)

if 'Sec_CFC' in model.sections.keys(): del model.sections['Sec_CFC']
model.HomogeneousSolidSection(name='Sec_CFC', material=mat_cfc_name, thickness=None)

# =====================================================
# 3. ASSIGN SECTIONS TO THE PARTS
# =====================================================

# Assign to TENDON
region_tendon = p_tendon.Set(elements=p_tendon.elements, name='SET_ALL_TENDON')
p_tendon.SectionAssignment(region=region_tendon, sectionName='Sec_Tendon', offset=0.0, 
                           offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

# Assign to UFC
region_ufc = p_ufc.Set(elements=p_ufc.elements, name='SET_ALL_UFC')
p_ufc.SectionAssignment(region=region_ufc, sectionName='Sec_UFC', offset=0.0, 
                        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

# Assign to CFC
region_cfc = p_cfc.Set(elements=p_cfc.elements, name='SET_ALL_CFC')
p_cfc.SectionAssignment(region=region_cfc, sectionName='Sec_CFC', offset=0.0, 
                        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

# =====================================================
# FINISH
# =====================================================
print('===================================================')
print('SCRIPT 02 FINISHED: Materials Created and Assigned!')
print('===================================================')
