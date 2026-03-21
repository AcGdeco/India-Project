import os
from build123d import *
from ocp_vscode import show

def check_geometric_identity(generated_part, file_path, tolerance=0.005):
    """
    Valida a identidade entre um modelo B-REP e um arquivo de referência.
    Auto-centraliza ambas as peças na origem (0,0,0) para garantir o alinhamento.
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

        # --- ESTRATÉGIA DE CENTRALIZAÇÃO ---
        # Movemos o centro geométrico de cada peça para a origem (0,0,0)
        # Isso ignora onde a origem estava no Inventor ou no Python.
        
        print("🔄 Alinhando centros geométricos...")
        shape_a_centered = shape_a.move(Location(-shape_a.bounding_box().center()))
        shape_b_centered = shape_b.move(Location(-shape_b.bounding_box().center()))

        # 3. Operação de Diferença Simétrica (XOR)
        # Usamos as versões centralizadas
        union_ab = shape_a_centered + shape_b_centered
        intersect_ab = shape_a_centered & shape_b_centered
        
        deviation_solid = union_ab - intersect_ab
        
        # 4. Cálculo do Volume Residual
        if isinstance(deviation_solid, ShapeList):
            residue_volume = sum(s.volume for s in deviation_solid)
        else:
            residue_volume = deviation_solid.volume
        
        # 5. Veredito
        if residue_volume <= tolerance:
            print(f"✅ SUCESSO: Geometrias coincidem.")
            print(f"Volume Residual: {residue_volume:.8f} mm³")
            return True
        else:
            print(f"❌ FALHA: Geometrias divergem.")
            print(f"Volume Residual: {residue_volume:.4f} mm³")
            # Mostra a peça A, a peça B e o erro para você comparar visualmente
            show(shape_a_centered, shape_b_centered, deviation_solid, 
                 names=["Python_Centered", "Inventor_Centered", "Diferenca_Erro"],
                 colors=["blue", "green", "red"], alphas=[0.5, 0.5, 1.0])
            return False

    except Exception as e:
        print(f"Erro Crítico na Comparação: {e}")
        return False