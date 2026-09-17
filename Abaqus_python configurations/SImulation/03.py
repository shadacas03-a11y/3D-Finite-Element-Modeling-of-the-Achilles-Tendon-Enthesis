from abaqus import *
from abaqusConstants import *

# =====================================================
# MODEL NAMES (Mapped to Centrale setup)
# =====================================================
MODEL_NAME = 'FInalModel'
model = mdb.models[MODEL_NAME]

MATERIAL_NAME = 'TENDON_HGO'
SECTION_NAME = 'Section_Tendon_HGO'

# =====================================================
# 1. CREATE THE SINGLE SECTION
# =====================================================
if SECTION_NAME in model.sections.keys():
    del model.sections[SECTION_NAME]

model.HomogeneousSolidSection(
    name=SECTION_NAME,
    material=MATERIAL_NAME,
    thickness=None
)

# =====================================================
# 2. ASSIGN SECTION TO ALL 3 PARTS
# =====================================================
# These match your imported part names in Abaqus
part_names = ['PART-1', 'PART-1_1', 'PART-1_2']

for p_name in part_names:
    p = model.parts[p_name]
    
    # Create Element Set
    set_name = 'ALL_ELEMENTS'
    if set_name in p.sets.keys():
        del p.sets[set_name]
        
    p.Set(name=set_name, elements=p.elements)
    
    # Delete previous assignments
    while len(p.sectionAssignments):
        del p.sectionAssignments[0]
        
    # Assign Section
    p.SectionAssignment(
        region=p.sets[set_name],
        sectionName=SECTION_NAME,
        offset=0.0,
        offsetType=MIDDLE_SURFACE,
        offsetField='',
        thicknessAssignment=FROM_SECTION
    )
    print('Assigned HGO Section to:', p_name)

print('--------------------------------')
print('SCRIPT 03 FINISHED:')
print('All 3 parts now use TENDON_HGO')
print('--------------------------------')
