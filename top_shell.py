from build123d import *
from ocp_vscode import show
from validador import check_geometric_identity

with BuildPart() as peca:
    # --- 1. MAIN SHELL BODY (LOFT) ---
    plano_base = Plane.XY
    plano_topo_loft = Plane.XY.offset(-3) 

    with BuildSketch(plano_base) as s1:
        r1 = Rectangle(129, 47)
        chamfer(r1.vertices(), length=8.671)
    
    with BuildSketch(plano_topo_loft) as s2:
        r2 = Rectangle(135, 53)
        chamfer(r2.vertices(), length=10.429)

    loft()

    # --- 2. MAIN ENCLOSURE WALL ---
    altura_1 = 9.824
    plano_topo_parede1 = Plane.XY.offset(-3 - altura_1)

    with BuildSketch(plano_topo_loft) as sk1:
        Rectangle(135, 53)
        chamfer(vertices(), length=10.429) 
        
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 2, 53 - 2)
            chamfer(vertices(), length=9.844)

    extrude(amount=-altura_1)

    # --- 3. D-PAD AREA CUTOUTS ---
    plano_rasgo = Plane.XY.offset(0)
    
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-38, 1)):
            Rectangle(29.999, 10.021)
    extrude(amount=-3, mode=Mode.SUBTRACT)

    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte2:
        with Locations((-38, 1)):
            Rectangle(10.021, 26.999)
    extrude(amount=-3, mode=Mode.SUBTRACT)

    # --- 4. D-PAD HOUSING (POSITIVE & NEGATIVE) ---
    plano_elevado = Plane.XY.offset(-3)
    with BuildSketch(plano_elevado):
        with Locations((-38, 1)):
            Ellipse(17.228, 15.4065)
    extrude(amount=-7.540)

    plano_corte = Plane.XY.offset(-3)
    with BuildSketch(plano_corte) as s_elipse:
        with Locations((-38, 1)):
            Ellipse(16.228, 14.4065)
    extrude(amount=-7.540, mode=Mode.SUBTRACT)

    # --- 5. INTERNAL MOUNTING PILLARS ---
    # Pillar 1 (Top Left)
    with Locations((-52.499, 13.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((-52.499, 13.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Pillar 2 (Top Right)
    with Locations((-52.499, -11.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((-52.499, -11.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Central Mounting Pillar
    with Locations((0, -11.5, -3)):
        Cylinder(radius=4, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((0, -11.5, -3)):
        Cylinder(radius=2.6, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Pillar 3 (Bottom Left)
    with Locations((52.499, 13.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((52.499, 13.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # Pillar 4 (Bottom Right)
    with Locations((52.499, -11.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((52.499, -11.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

    # --- 6. ACTION BUTTONS CLUSTERS ---
    button_positions = [(28.005, 1), (48.006, 1), (38.006, 9.5), (38.006, -7.5)]

    for pos in button_positions:
        with Locations((pos[0], pos[1], 0)):
            Cylinder(radius=5, height=3, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
        
        with Locations((pos[0], pos[1], -3)):
            Cylinder(radius=6, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MAX))
        with Locations((pos[0], pos[1], -3)):
            Cylinder(radius=5, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
        
        plano_guide = Plane.XY.offset(-3)
        with BuildSketch(plano_guide) as s_guide:
            with Locations(pos):
                Rectangle(2, 12)
                Rectangle(12, 2)
        extrude(amount=-9.474, mode=Mode.SUBTRACT)

    # --- 7. INTERNAL REINFORCEMENT WALLS ---
    plano_internal = Plane.XY.offset(-3)

    with BuildSketch(plano_internal) as s_wall1:
        with Locations((-0, 3.547)):
            Rectangle(35.239, 2)
    extrude(amount=-11.824)

    with BuildSketch(plano_internal) as s_wall2:
        with Locations((-16.6195, 14.0235)):
            Rectangle(2, 18.953)
        with Locations((16.6195, 14.0235)):
            Rectangle(2, 18.953)
    extrude(amount=-11.824)

    # --- 8. FINAL SLOT CUTOUT ---
    plano_base_cut = Plane.XY.offset(0)
    with BuildSketch(plano_base_cut) as s_final:
        with Locations((0, 25)):
            Rectangle(37.039, 3)
    extrude(amount=-12.824, mode=Mode.SUBTRACT)

# --- 9. VIEW AND EXPORT ---
show(peca)
export_step(peca.part, "top_shell.step")
print("Success! 'top_shell.step' has been created.")

result = check_geometric_identity(peca, "RetroPad - Top Shell.stl")