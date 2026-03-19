from build123d import *
from ocp_vscode import show

# Criando uma peça com um cilindro e um tronco de cilindro no topo
with BuildPart() as peca_teste:
    # Base do cilindro principal
    Cylinder(
        radius=4.8,
        height=14.5,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # Tronco no topo: base 4.8 mm, topo 3.8 mm, altura 5 mm
    with Locations((0, 0, 14.5)):
        Cone(
            bottom_radius=4.8,
            top_radius=3.8,
            height=1,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

    # Base do box lateral
    with Locations((5.315, 0, 0)):
        Box(
            1.2, 
            1.8, 
            5.5, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # Base do box lateral
    with Locations((-5.315, 0, 0)):
        Box(
            1.2, 
            1.8, 
            5.5, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )    

    # Base do box lateral
    with Locations((0, 5.315, 0)):
        Box(
            1.8,
            1.2, 
            5.5, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )   

    # Base do box lateral
    with Locations((0, -5.315, 0)):
        Box(
            1.8,
            1.2, 
            5.5, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )  

# Envia a peça para o painel lateral do VS Code
show(peca_teste)