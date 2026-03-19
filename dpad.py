from build123d import *
from ocp_vscode import show

# Criando uma peça com um cilindro e um tronco de cilindro no topo
with BuildPart() as dpad:
    
    # Base elíptica principal (semi-eixos X e Y)
    with BuildSketch():
        Ellipse(16.150, 14.209)

    # Extrusão da base
    extrude(amount=4.5)

    # box
    with Locations((0, 0, 4.5)):
        Box(
            9.399,
            26.400, 
            2, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # box
    with Locations((0, 0, 4.5)):
        Box(
            29.399, 
            9.421,
            2, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

        # box
    with Locations((0, 0, -4.5)):
        Box(
            9.399, 
            26.400,
            8, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

        # box
    with Locations((0, 0, -4.5)):
        Box(
            29.399, 
            9.421,
            8, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    with BuildPart() as peca:
        # 1. Criamos os dois perfis (as "fatias" do tronco)
        # O primeiro no chão (Z=0) e o segundo no topo (Z=5)
        plano_base = Plane.XY
        plano_topo = Plane.XY.offset(-0.974) # Altura de 5mm conforme seu comentário

        # 2. Desenhamos os retângulos nesses planos
        with BuildSketch(plano_base) as s1:
            Rectangle(29.399, 9.421) # Base de 4.8mm
        
        with BuildSketch(plano_topo) as s2:
            Rectangle(27.399, 7.421) # Topo de 3.8mm

        # 3. O comando Loft une os dois sketches criando o sólido
        loft()

        # Para posicionar no seu projeto na altura específica:
        peca.part.move(Location((0, 0, - 4.5)))

    with BuildPart() as peca:
        # 1. Criamos os dois perfis (as "fatias" do tronco)
        # O primeiro no chão (Z=0) e o segundo no topo (Z=5)
        plano_base = Plane.XY
        plano_topo = Plane.XY.offset(-0.974) # Altura de 5mm conforme seu comentário

        # 2. Desenhamos os retângulos nesses planos
        with BuildSketch(plano_base) as s1:
            Rectangle(9.399, 26.400) # Base de 4.8mm
        
        with BuildSketch(plano_topo) as s2:
            Rectangle(7.399, 24.400) # Topo de 3.8mm

        # 3. O comando Loft une os dois sketches criando o sólido
        loft()

        # Para posicionar no seu projeto na altura específica:
        peca.part.move(Location((0, 0, - 4.5)))
    
# Envia a peça para o painel lateral do VS Code
show(dpad)