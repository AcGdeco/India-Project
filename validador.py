import os
from build123d import *
from ocp_vscode import show

def check_geometric_identity(generated_part, file_path, tolerance=0.005):
    """
    Valida a identidade entre um modelo B-REP e um arquivo de referência.
    Compara volume, área e dimensões do bounding box.
    """
    if not os.path.exists(file_path):
        print(f"❌ Erro: Arquivo {file_path} não encontrado.")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ Erro: O arquivo está vazio (0 KB).")
        return False

    try:
        # 1. Importação da Referência (Peça B)
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.step', '.stp']:
            shape_b = import_step(file_path)
        else:
            imported_mesh = Mesher().read(file_path)[0]
            try:
                shape_b = Solid.make_solid(imported_mesh).fix()
            except:
                shape_b = imported_mesh

        # 2. Preparação da Peça Gerada (Peça A)
        if hasattr(generated_part, "part"):
            shape_a = generated_part.part
        else:
            shape_a = generated_part

        if hasattr(shape_a, "solid"):
            shape_a = shape_a.solid()

        # 3. Comparação por Volume
        print("🔄 Comparando volumes...")
        vol_a = shape_a.volume
        vol_b = shape_b.volume
        vol_diff = abs(vol_a - vol_b)
        vol_diff_pct = (vol_diff / vol_b * 100) if vol_b != 0 else float('inf')

        print(f"   Volume A (Python): {vol_a:.4f} mm³")
        print(f"   Volume B (STL):    {vol_b:.4f} mm³")
        print(f"   Diferença:         {vol_diff:.4f} mm³ ({vol_diff_pct:.4f}%)")

        # 4. Comparação por Bounding Box
        print("🔄 Comparando bounding boxes...")

        def get_dims(shape):
            bb = shape.bounding_box()
            return {
                "X": round(bb.max.X - bb.min.X, 4),
                "Y": round(bb.max.Y - bb.min.Y, 4),
                "Z": round(bb.max.Z - bb.min.Z, 4),
            }

        dims_a = get_dims(shape_a)
        dims_b = get_dims(shape_b)

        print(f"   Dimensões A: X={dims_a['X']} Y={dims_a['Y']} Z={dims_a['Z']}")
        print(f"   Dimensões B: X={dims_b['X']} Y={dims_b['Y']} Z={dims_b['Z']}")

        dim_ok = all(abs(dims_a[k] - dims_b[k]) <= tolerance * 100 for k in ["X", "Y", "Z"])

        # 5. Comparação por Área de Superfície
        print("🔄 Comparando áreas de superfície...")
        area_a = shape_a.area
        area_b = shape_b.area
        area_diff_pct = (abs(area_a - area_b) / area_b * 100) if area_b != 0 else float('inf')

        print(f"   Área A (Python): {area_a:.4f} mm²")
        print(f"   Área B (STL):    {area_b:.4f} mm²")
        print(f"   Diferença:       {area_diff_pct:.4f}%")

        # 6. Veredito
        vol_ok  = vol_diff_pct  <= 1.0   # tolerância 1%
        area_ok = area_diff_pct <= 2.0   # tolerância 2% (STL tem aproximação de malha)

        if vol_ok and dim_ok and area_ok:
            print(f"✅ SUCESSO: Geometrias coincidem.")
            return True
        else:
            print(f"❌ FALHA: Geometrias divergem.")
            if not vol_ok:
                print(f"   → Volume fora da tolerância ({vol_diff_pct:.2f}%)")
            if not dim_ok:
                print(f"   → Dimensões fora da tolerância: A={dims_a} B={dims_b}")
            if not area_ok:
                print(f"   → Área fora da tolerância ({area_diff_pct:.2f}%)")
            show(shape_a, shape_b,
                 names=["Python", "Referencia_STL"],
                 colors=["blue", "green"], alphas=[0.5, 0.5])
            return False

    except Exception as e:
        print(f"Erro Crítico na Comparação: {e}")
        import traceback
        traceback.print_exc()
        return False