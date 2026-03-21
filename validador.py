import os
from build123d import *
from ocp_vscode import show

def check_geometric_identity(generated_part, file_path, tolerance=0.005):
    """
    Validates the geometric identity between a B-REP model and a reference file.
    Compares volume, surface area, and bounding box dimensions.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found.")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ Error: File is empty (0 KB).")
        return False

    try:
        # 1. Import the reference shape (Shape B)
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.step', '.stp']:
            shape_b = import_step(file_path)
        else:
            imported_mesh = Mesher().read(file_path)[0]
            try:
                shape_b = Solid.make_solid(imported_mesh).fix()
            except:
                shape_b = imported_mesh

        # 2. Prepare the generated part (Shape A)
        if hasattr(generated_part, "part"):
            shape_a = generated_part.part
        else:
            shape_a = generated_part

        if hasattr(shape_a, "solid"):
            shape_a = shape_a.solid()

        # 3. Volume comparison
        print("🔄 Comparing volumes...")
        vol_a = shape_a.volume
        vol_b = shape_b.volume
        vol_diff = abs(vol_a - vol_b)
        vol_diff_pct = (vol_diff / vol_b * 100) if vol_b != 0 else float('inf')

        print(f"   Volume A (Python): {vol_a:.4f} mm³")
        print(f"   Volume B (STL):    {vol_b:.4f} mm³")
        print(f"   Difference:        {vol_diff:.4f} mm³ ({vol_diff_pct:.4f}%)")

        # 4. Bounding box comparison
        print("🔄 Comparing bounding boxes...")

        def get_dims(shape):
            bb = shape.bounding_box()
            return {
                "X": round(bb.max.X - bb.min.X, 4),
                "Y": round(bb.max.Y - bb.min.Y, 4),
                "Z": round(bb.max.Z - bb.min.Z, 4),
            }

        dims_a = get_dims(shape_a)
        dims_b = get_dims(shape_b)

        print(f"   Dimensions A: X={dims_a['X']} Y={dims_a['Y']} Z={dims_a['Z']}")
        print(f"   Dimensions B: X={dims_b['X']} Y={dims_b['Y']} Z={dims_b['Z']}")

        # All axes must be within tolerance * 100 mm
        dim_ok = all(abs(dims_a[k] - dims_b[k]) <= tolerance * 100 for k in ["X", "Y", "Z"])

        # 5. Surface area comparison
        print("🔄 Comparing surface areas...")
        area_a = shape_a.area
        area_b = shape_b.area
        area_diff_pct = (abs(area_a - area_b) / area_b * 100) if area_b != 0 else float('inf')

        print(f"   Area A (Python): {area_a:.4f} mm²")
        print(f"   Area B (STL):    {area_b:.4f} mm²")
        print(f"   Difference:      {area_diff_pct:.4f}%")

        # 6. Verdict
        vol_ok  = vol_diff_pct  <= 1.0   # 1% tolerance
        area_ok = area_diff_pct <= 2.0   # 2% tolerance (STL mesh approximation)

        if vol_ok and dim_ok and area_ok:
            print(f"✅ SUCCESS: Geometries match.")
            return True
        else:
            print(f"❌ FAILURE: Geometries diverge.")
            if not vol_ok:
                print(f"   → Volume out of tolerance ({vol_diff_pct:.2f}%)")
            if not dim_ok:
                print(f"   → Dimensions out of tolerance: A={dims_a} B={dims_b}")
            if not area_ok:
                print(f"   → Surface area out of tolerance ({area_diff_pct:.2f}%)")
            # Display both shapes and the deviation for visual inspection
            show(shape_a, shape_b,
                 names=["Python", "Reference_STL"],
                 colors=["blue", "green"], alphas=[0.5, 0.5])
            return False

    except Exception as e:
        print(f"Critical Error during comparison: {e}")
        import traceback
        traceback.print_exc()
        return False