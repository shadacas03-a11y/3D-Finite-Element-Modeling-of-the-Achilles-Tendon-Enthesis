SetFactory("Built-in");

Merge "Tendon_body_meshlab.stl";

// Maximum angle (Pi) to ensure a perfectly smooth skin with no artificial lines
ClassifySurfaces{Pi, 1, 1, Pi};
CreateGeometry;

Surface Loop(1) = Surface{:};
Volume(1) = {1};
Physical Volume("TENDON_BODY") = {1};

// --- STRICT 1.0mm GLOBAL SEED ---
Mesh.MeshSizeMin = 1.0;
Mesh.MeshSizeMax = 1.0;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;
Mesh.MeshSizeExtendFromBoundary = 0;

// --- THE VISUAL FIX ---
// Algorithm 6 forces perfect, uniform surface triangles (like the guide)
Mesh.Algorithm = 6; 
// Algorithm 1 fills the inside reliably
Mesh.Algorithm3D = 1;

// Maximum optimization to prevent degenerate elements
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Smoothing = 100;

// CRITICAL: Set to 0 to only export the 3D solid, preventing the Abaqus wireframe error
Mesh.SaveAll = 0; 

