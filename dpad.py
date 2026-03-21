from build123d import *
from ocp_vscode import show
from validador import check_geometric_identity

# --- CÓDIGO ORIGINAL (SEM ALTERAÇÕES NAS MEDIDAS) ---
with BuildPart() as dpad:
    with BuildSketch(Plane.XY.offset(8)):
        Ellipse(16.150, 14.209)
    extrude(amount=4.5)

    with Locations((0, 0, 12.5)):
        Box(9.399, 26.400, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(29.399, 9.421, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with Locations((0, 0, 0)):
        Box(9.399, 26.400, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(29.399, 9.421, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with BuildPart() as horizontal_loft:
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974)
        with BuildSketch(base_plane) as s1:
            Rectangle(29.399, 9.421)
        with BuildSketch(top_plane) as s2:
            Rectangle(27.399, 7.421)
        loft()
        horizontal_loft.part.move(Location((0, 0, 0)))

    with BuildPart() as vertical_loft:
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974)
        with BuildSketch(base_plane) as s1:
            Rectangle(9.399, 26.400)
        with BuildSketch(top_plane) as s2:
            Rectangle(7.399, 24.400)
        loft()
        vertical_loft.part.move(Location((0, 0, 0)))

# --- ORIENTAÇÃO E Z (TRANSFORMAÇÃO FINAL) ---

# 1. Pegamos a parte final
final_part = dpad.part

# 2. Giramos 180 graus no eixo X (Ponta cabeça)
# 3. Movemos para compensar a altura (o ponto mais alto era 14.5, agora será o chão)
dpad_inverted = final_part.rotate(Axis.X, 180).move(Location((0, 0, 14.5)))

# Visualização da peça invertida
show(dpad_inverted)

# Validação (Lembre-se de girar o STL no Inventor também para bater)
result = check_geometric_identity(dpad_inverted, "RetroPad - D-Pad.stl")