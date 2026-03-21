import os
from build123d import *
from ocp_vscode import show

def check_geometric_identity(generated_part, file_path, tolerance=0.005):
    """
    Valida a identidade entre um modelo B-REP e um arquivo de referência (STL ou STEP).
    Detecta a extensão do arquivo e aplica o método de importação correto.
    """
    # 1. Verificação de existência e integridade
    if not os.path.exists(file_path):
        print(f"❌ Erro: Arquivo {file_path} não encontrado.")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ Erro: O arquivo está vazio (0 KB).")
        return False

    try:
        # 2. Identificação da Extensão e Importação
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.step', '.stp']:
            # Importação de Sólido Analítico (B-REP)
            shape_b = import_step(file_path)
            print(f"📦 Arquivo STEP carregado com sucesso.")
        else:
            # Importação de Malha (STL)
            imported_mesh = Mesher().read(file_path)[0]
            try:
                shape_b = Solid.make_solid(imported_mesh).fix()
            except:
                shape_b = imported_mesh
            print(f"🕸️ Arquivo STL carregado (conversão para sólido tentada).")

        # --- Detecção do Componente Gerado (A) ---
        if hasattr(generated_part, "part"):
            shape_a = generated_part.part
        else:
            shape_a = generated_part
            
        # 3. Operação de Diferença Simétrica (XOR Geométrico)
        # O resultado é o volume que não é comum entre as duas peças
        union_ab = shape_a + shape_b
        intersect_ab = shape_a & shape_b
        
        deviation_solid = union_ab - intersect_ab
        
        # 4. Cálculo do Volume Residual
        if isinstance(deviation_solid, ShapeList):
            residue_volume = sum(s.volume for s in deviation_solid)
        else:
            residue_volume = deviation_solid.volume
        
        # 5. Veredito
        if residue_volume <= tolerance:
            print(f"✅ SUCESSO: Geometrias são idênticas.")
            print(f"Volume Residual: {residue_volume:.8f} mm³")
            return True
        else:
            print(f"❌ FALHA: Geometrias divergem.")
            print(f"Volume Residual: {residue_volume:.4f} mm³")
            # Mostra o erro no OCP Viewer (em vermelho as partes que não batem)
            show(deviation_solid, names=["Desvio_Residuo"])
            return False

    except Exception as e:
        print(f"Erro Crítico na Comparação: {e}")
        return False