from build123d import *
from ocp_vscode import show

with BuildPart() as peca:
    # --- 1. CORPO BASE (LOFT) ---
    plano_base = Plane.XY
    plano_topo_loft = Plane.XY.offset(3) 

    with BuildSketch(plano_base) as s1:
        r1 = Rectangle(47, 129)
        chamfer(r1.vertices(), length=8.671)
    
    with BuildSketch(plano_topo_loft) as s2:
        r2 = Rectangle(53, 135)
        chamfer(r2.vertices(), length=10.429)

    loft()

    altura_1 = 9.824
    plano_topo_parede1 = Plane.XY.offset(3 + altura_1)

    with BuildSketch(plano_topo_loft) as sk1:
        # 1. Perímetro Externo
        Rectangle(53, 135)
        chamfer(vertices(), length=10.429) 
        
        # 2. Perímetro Interno (Subtração para criar a parede)
        with BuildSketch(mode=Mode.SUBTRACT):
            # Recuo de 2mm em cada lado (53-4 e 135-4)
            Rectangle(53 - 2, 135 - 2)
            # Para 2mm reais no chanfro de 45 graus: 10.429 - (2 * sqrt(2))
            chamfer(vertices(), length=9.844)

    extrude(amount=altura_1)

    # --- SUBTRAÇÃO DE RASGO COM EXTRUDE ---
    # Criamos um plano de trabalho na altura Z=4.6
    plano_rasgo = Plane.XY.offset(0)
    
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-1, 38)):
            Rectangle(10.021, 29.999)
    
    # O extrude aqui vai "perfurar" a peça 14.824mm para cima
    extrude(amount=3, mode=Mode.SUBTRACT)

    # --- SUBTRAÇÃO DE RASGO COM EXTRUDE ---
    # Criamos um plano de trabalho na altura Z=4.6
    plano_rasgo = Plane.XY.offset(0)
    
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-1, 38)):
            Rectangle(26.999, 10.021)
    
    # O extrude aqui vai "perfurar" a peça 14.824mm para cima
    extrude(amount=3, mode=Mode.SUBTRACT)

    # 1. Definimos o plano deslocado em 3mm no eixo Z
    plano_elevado = Plane.XY.offset(3)

    # 2. Criamos o sketch nesse plano
    with BuildSketch(plano_elevado):
        # Note que no Locations agora usamos apenas (X, Y) 
        # pois o Z já está definido pelo plano.
        with Locations((-1, 38)):
            Ellipse(15.4065, 17.228)

    # 3. A extrusão partirá de Z=3 e subirá 4.5mm (terminando em Z=7.5)
    extrude(amount=7.540)

    # 1. Criamos um plano de referência deslocado 3mm para cima
    plano_corte = Plane.XY.offset(3)

    # 2. Iniciamos o Sketch neste plano elevado
    with BuildSketch(plano_corte) as s_elipse:
        # No Locations de um Sketch (2D), passamos apenas X e Y
        with Locations((-1, 38)):
            Ellipse(14.4065, 16.228)

    # 3. O extrude agora "fura" a peça a partir de Z=3, subindo 4.5mm
    # Ele vai remover material entre Z=3 e Z=7.5
    extrude(amount=7.540, mode=Mode.SUBTRACT)

    # --- ADICIONANDO OU SUBTRAINDO CILINDRO ---
    # Se quiser que ele subtraia, use mode=Mode.SUBTRACT no Cylinder
    with Locations((-13.5, 52.499, 3)):
        Cylinder(
            radius=2.5,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((-13.5, 52.499, 3)):
        Cylinder(
            radius=1.100,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((11.5, 52.499, 3)):
        Cylinder(
            radius=2.5,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((11.5, 52.499, 3)):
        Cylinder(
            radius=1.100,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )
    # Furo central
    with Locations((11.5, 0, 3)):
        Cylinder(
            radius=4,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((11.5, 0, 3)):
        Cylinder(
            radius=2.6,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Laterais
    with Locations((-13.5, -52.499, 3)):
        Cylinder(
            radius=2.5,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((-13.5, -52.499, 3)):
        Cylinder(
            radius=1.100,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((11.5, -52.499, 3)):
        Cylinder(
            radius=2.5,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((11.5, -52.499, 3)):
        Cylinder(
            radius=1.100,
            height=11.824, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Buttons Holes
    with Locations((-1, -28.005, 0)):
        Cylinder(
            radius=5,
            height=3, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Wall Holes
    with Locations((-1, -28.005, 3)):
        Cylinder(
            radius=6,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((-1, -28.005, 3)):
        Cylinder(
            radius=5,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )   

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-1, -28.005)):
            Rectangle(12, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-1, -28.005)):
            Rectangle(2, 12)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Buttons Holes
    with Locations((-1, -48.006, 0)):
        Cylinder(
            radius=5,
            height=3, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Wall Holes
    with Locations((-1, -48.006, 3)):
        Cylinder(
            radius=6,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((-1, -48.006, 3)):
        Cylinder(
            radius=5,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )   

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-1, -48.006)):
            Rectangle(12, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-1, -48.006)):
            Rectangle(2, 12)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Buttons Holes
    with Locations((-9.5, -38.006, 0)):
        Cylinder(
            radius=5,
            height=3, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Wall Holes
    with Locations((-9.5, -38.006, 3)):
        Cylinder(
            radius=6,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((-9.5, -38.006, 3)):
        Cylinder(
            radius=5,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )   

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-9.5, -38.006)):
            Rectangle(12, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-9.5, -38.006)):
            Rectangle(2, 12)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Buttons Holes
    with Locations((7.5, -38.006, 0)):
        Cylinder(
            radius=5,
            height=3, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Wall Holes
    with Locations((7.5, -38.006, 3)):
        Cylinder(
            radius=6,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    with Locations((7.5, -38.006, 3)):
        Cylinder(
            radius=5,
            height=7.474, 
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT
            # mode=Mode.SUBTRACT  <-- Adicione isso se quiser furar a peça
        )

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((7.5, -38.006)):
            Rectangle(12, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((7.5, -38.006)):
            Rectangle(2, 12)
    
    # O extrude cria a profundidade do furo
    extrude(amount=9.474, mode=Mode.SUBTRACT)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    # Criamos o plano no Z=3
    plano_rasgo = Plane.XY.offset(3)

    # Wall
    with BuildSketch(plano_rasgo) as s2:
        with Locations((-3.547, 0)):
            Rectangle(2, 35.239)
    
    # O extrude cria a profundidade do furo
    extrude(amount=11.824)

    with BuildSketch(plano_rasgo) as s2:
        with Locations((-14.0235, 16.6195)):
            Rectangle(18.953, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=11.824)

    # Wall
    with BuildSketch(plano_rasgo) as s2:
        with Locations((-14.0235, -16.6195)):
            Rectangle(18.953, 2)
    
    # O extrude cria a profundidade do furo
    extrude(amount=11.824)

    # Criamos o plano no Z=0
    plano_rasgo = Plane.XY.offset(0)

    # Wall Cut
    with BuildSketch(plano_rasgo) as s2:
        with Locations((-25, 0)):
            Rectangle(3, 37.039)
    
    # O extrude cria a profundidade do furo
    extrude(amount=12.824, mode=Mode.SUBTRACT)

# Visualização
show(peca)

# 1. Exportando a peça completa (o sólido resultante)
export_step(peca.part, "top_shell.step")

print("Sucesso! O arquivo 'top_shell.step' foi criado na sua pasta.")