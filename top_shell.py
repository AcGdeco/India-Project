from build123d import *
from ocp_vscode import show

with BuildPart() as peca:
    # --- 1. MAIN SHELL BODY (LOFT) ---
    # Defining planes for the base and the top transition of the loft
    plano_base = Plane.XY
    plano_topo_loft = Plane.XY.offset(3) 

    with BuildSketch(plano_base) as s1:
        r1 = Rectangle(47, 129)
        chamfer(r1.vertices(), length=8.671)
    
    with BuildSketch(plano_topo_loft) as s2:
        r2 = Rectangle(53, 135)
        chamfer(r2.vertices(), length=10.429)

    loft()

    # --- 2. MAIN ENCLOSURE WALL ---
    # Creating the vertical wall with a constant thickness using subtraction
    altura_1 = 9.824
    plano_topo_parede1 = Plane.XY.offset(3 + altura_1)

    with BuildSketch(plano_topo_loft) as sk1:
        # Outer perimeter
        Rectangle(53, 135)
        chamfer(vertices(), length=10.429) 
        
        # Inner perimeter (Subtracting to hollow out the part)
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(53 - 2, 135 - 2)
            chamfer(vertices(), length=9.844)

    extrude(amount=altura_1)

    # --- 3. D-PAD AREA CUTOUTS ---
    # Rectangular cross cutouts for D-pad clearance at Z=0
    plano_rasgo = Plane.XY.offset(0)
    
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-1, 38)):
            Rectangle(10.021, 29.999)
    extrude(amount=3, mode=Mode.SUBTRACT)

    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte2:
        with Locations((-1, 38)):
            Rectangle(26.999, 10.021)
    extrude(amount=3, mode=Mode.SUBTRACT)

    # --- 4. D-PAD HOUSING (POSITIVE & NEGATIVE) ---
    # Creating the elevated elliptical housing for the D-pad
    plano_elevado = Plane.XY.offset(3)
    with BuildSketch(plano_elevado):
        with Locations((-1, 38)):
            Ellipse(15.4065, 17.228)
    extrude(amount=7.540)

    # Hollow out the elliptical housing
    plano_corte = Plane.XY.offset(3)
    with BuildSketch(plano_corte) as s_elipse:
        with Locations((-1, 38)):
            Ellipse(14.4065, 16.228)
    extrude(amount=7.540, mode=Mode.SUBTRACT)

    # --- 5. INTERNAL MOUNTING PILLARS ---
    # Cylindrical supports and holes for PCB/Screen mounting
    
    # Pillar 1 (Top Left)
    with Locations((-13.5, 52.499, 3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-13.5, 52.499, 3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Pillar 2 (Top Right)
    with Locations((11.5, 52.499, 3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((11.5, 52.499, 3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Central Mounting Pillar
    with Locations((11.5, 0, 3)):
        Cylinder(radius=4, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((11.5, 0, 3)):
        Cylinder(radius=2.6, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Pillar 3 (Bottom Left)
    with Locations((-13.5, -52.499, 3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-13.5, -52.499, 3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Pillar 4 (Bottom Right)
    with Locations((11.5, -52.499, 3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((11.5, -52.499, 3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # --- 6. ACTION BUTTONS CLUSTERS ---
    # Creating holes and recessed walls for 4 action buttons
    button_positions = [(-1, -28.005), (-1, -48.006), (-9.5, -38.006), (7.5, -38.006)]

    for pos in button_positions:
        # Thru-hole for button
        with Locations((pos[0], pos[1], 0)):
            Cylinder(radius=5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        
        # Recessed wall for button mechanism
        with Locations((pos[0], pos[1], 3)):
            Cylinder(radius=6, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((pos[0], pos[1], 3)):
            Cylinder(radius=5, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        
        # Mechanical guides (cross-shaped slots)
        plano_guide = Plane.XY.offset(3)
        with BuildSketch(plano_guide) as s_guide:
            with Locations(pos):
                Rectangle(12, 2)
                Rectangle(2, 12)
        extrude(amount=9.474, mode=Mode.SUBTRACT)

    # --- 7. INTERNAL REINFORCEMENT WALLS ---
    # Structural walls to support internal components
    plano_internal = Plane.XY.offset(3)

    # Vertical reinforcement wall
    with BuildSketch(plano_internal) as s_wall1:
        with Locations((-3.547, 0)):
            Rectangle(2, 35.239)
    extrude(amount=11.824)

    # Horizontal reinforcement walls
    with BuildSketch(plano_internal) as s_wall2:
        with Locations((-14.0235, 16.6195)):
            Rectangle(18.953, 2)
        with Locations((-14.0235, -16.6195)):
            Rectangle(18.953, 2)
    extrude(amount=11.824)

    # --- 8. FINAL SLOT CUTOUT ---
    # Large slot cutout at the base (Z=0)
    plano_base_cut = Plane.XY.offset(0)
    with BuildSketch(plano_base_cut) as s_final:
        with Locations((-25, 0)):
            Rectangle(3, 37.039)
    extrude(amount=12.824, mode=Mode.SUBTRACT)

# --- 9. VIEW AND EXPORT ---
show(peca)
export_step(peca.part, "top_shell.step")
print("Success! 'top_shell.step' has been created.")