from build123d import *
from ocp_vscode import show

# =============================================================================
# --- BOTTOM SHELL ---
# =============================================================================
with BuildPart() as bottom_shell:
    # Base plane at Z=0, loft top plane at Z=3
    base_plane = Plane.XY
    loft_top_plane = Plane.XY.offset(3)

    # Bottom face sketch — smaller rectangle at Z=0
    with BuildSketch(base_plane) as s1:
        r1 = Rectangle(129, 47)
        chamfer(r1.vertices(), length=8.671)
    # Top face sketch — larger rectangle at Z=3 for the loft transition
    with BuildSketch(loft_top_plane) as s2:
        r2 = Rectangle(135, 53)
        chamfer(r2.vertices(), length=10.429)
    loft()

    # First hollow wall — 2mm constant thickness, extruded 6.6mm upward
    height_1 = 6.6
    wall1_top_plane = Plane.XY.offset(3 + height_1)
    with BuildSketch(loft_top_plane) as sk1:
        # Outer perimeter
        Rectangle(135, 53)
        chamfer(vertices(), length=10.429)
        # Inner perimeter subtracted to create 2mm wall thickness
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 4, 53 - 4)
            chamfer(vertices(), length=9.258)
    extrude(amount=height_1)

    # Second hollow wall — 1mm step inward, extruded 9.824mm upward
    # Creates the ledge for the top shell to seat onto
    with BuildSketch(wall1_top_plane) as sk2:
        Rectangle(135 - 2, 53 - 2)
        chamfer(vertices(), length=9.845)
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 4, 53 - 4)
            chamfer(vertices(), length=9.258)
    extrude(amount=9.824)

    # Internal support pillars — solid base (radius 2.5, 3mm tall) at Z=3
    # topped by a thin pin (radius 1, 13.424mm tall) starting at Z=6
    # Top Right Pillar
    with Locations((52.5, 13.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((52.5, 13.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Top Left Pillar
    with Locations((-52.5, 13.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, 13.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Bottom Right Pillar
    with Locations((52.5, -11.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((52.5, -11.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Bottom Left Pillar
    with Locations((-52.5, -11.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, -11.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    # Central Pillar — larger base radius for extra structural support
    with Locations((0, -11.5, 3)):
        Cylinder(radius=4, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, -11.5, 6)):
        Cylinder(radius=2.5, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Hollow elliptical collars on the loft top face — left and right sides
    # Used as alignment or retention features for internal components
    ellipse_plane = Plane.XY.offset(3)
    # Right-side ellipse collar (positive X)
    with BuildSketch(ellipse_plane) as s_elipse1:
        with Locations((38, 1)):
            Ellipse(10.5, 9)
            with BuildSketch(mode=Mode.SUBTRACT):
                with Locations((38, 1)):
                    Ellipse(9.5, 8)
    extrude(amount=3)
    # Left-side ellipse collar (negative X)
    with BuildSketch(ellipse_plane) as s_elipse2:
        with Locations((-38, 1)):
            Ellipse(10.5, 9)
            with BuildSketch(mode=Mode.SUBTRACT):
                with Locations((-38, 1)):
                    Ellipse(9.5, 8)
    extrude(amount=3)

    # Rectangular slot cut starting at Z=4.6, perforating 14.824mm upward
    # Used for cable routing or internal component clearance
    slot_plane = Plane.XY.offset(4.6)
    with BuildSketch(slot_plane, mode=Mode.SUBTRACT) as s_cut:
        with Locations((0, 25.5)):
            Rectangle(37.039, 2)
    extrude(amount=14.824, mode=Mode.SUBTRACT)

# Z position where the top shell seats onto the bottom shell
# Base height (19.424mm) + cumulative vertical offset adjustments (+3mm)
bottom_top_z = 3 + 6.6 + 9.824 + 2 + 1  # = 22.424

# =============================================================================
# --- TOP SHELL ---
# =============================================================================
with BuildPart() as top_shell:
    # Base plane at Z=0 (external face), loft top plane 3mm downward
    base_plane = Plane.XY
    plano_topo_loft = Plane.XY.offset(-3)

    # External face sketch at Z=0
    with BuildSketch(base_plane) as s1:
        r1 = Rectangle(129, 47)
        chamfer(r1.vertices(), length=8.671)
    # Inner loft face sketch at Z=-3
    with BuildSketch(plano_topo_loft) as s2:
        r2 = Rectangle(135, 53)
        chamfer(r2.vertices(), length=10.429)
    loft()

    # Main enclosure wall — single thickness, extruded 9.824mm downward
    altura_1 = 9.824
    with BuildSketch(plano_topo_loft) as sk1:
        # Outer wall perimeter
        Rectangle(135, 53)
        chamfer(vertices(), length=10.429)
        # Inner perimeter subtracted to hollow out the wall
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 2, 53 - 2)
            chamfer(vertices(), length=9.844)
    extrude(amount=-altura_1)

    # Cross-shaped D-pad cutout through the base face at Z=0
    plano_rasgo = Plane.XY.offset(0)
    # Horizontal slot
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-38, 1)):
            Rectangle(29.999, 10.021)
    extrude(amount=-3, mode=Mode.SUBTRACT)
    # Vertical slot
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte2:
        with Locations((-38, 1)):
            Rectangle(10.021, 26.999)
    extrude(amount=-3, mode=Mode.SUBTRACT)

    # Elliptical D-pad housing — hollow collar extruded 7.54mm downward
    plano_elevado = Plane.XY.offset(-3)
    # Outer elliptical wall
    with BuildSketch(plano_elevado):
        with Locations((-38, 1)):
            Ellipse(17.228, 15.4065)
    extrude(amount=-7.540)
    # Inner ellipse subtracted to create the hollow housing
    plano_corte = Plane.XY.offset(-3)
    with BuildSketch(plano_corte) as s_elipse:
        with Locations((-38, 1)):
            Ellipse(16.228, 14.4065)
    extrude(amount=-7.540, mode=Mode.SUBTRACT)

    # Hollow mounting pillars — grow downward from Z=-3 using Align.MAX
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
    # Central Mounting Pillar (larger radius for central PCB support)
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

    # Action button holes with recessed walls and cross-shaped guide slots
    button_positions = [(28.005, 1), (48.006, 1), (38.006, 9.5), (38.006, -7.5)]
    for pos in button_positions:
        # Through-hole in the base face for the button shaft
        with Locations((pos[0], pos[1], 0)):
            Cylinder(radius=5, height=3, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
        # Recessed cylindrical wall around the button opening
        with Locations((pos[0], pos[1], -3)):
            Cylinder(radius=6, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MAX))
        with Locations((pos[0], pos[1], -3)):
            Cylinder(radius=5, height=7.474, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
        # Cross-shaped guide slots for button alignment tabs
        plano_guide = Plane.XY.offset(-3)
        with BuildSketch(plano_guide) as s_guide:
            with Locations(pos):
                Rectangle(2, 12)
                Rectangle(12, 2)
        extrude(amount=-9.474, mode=Mode.SUBTRACT)

    # Central vertical reinforcement rib
    plano_internal = Plane.XY.offset(-3)
    with BuildSketch(plano_internal) as s_wall1:
        with Locations((0, 3.547)):
            Rectangle(35.239, 2)
    extrude(amount=-11.824)
    # Left and right horizontal reinforcement ribs
    with BuildSketch(plano_internal) as s_wall2:
        with Locations((-16.6195, 14.0235)):
            Rectangle(2, 18.953)
        with Locations((16.6195, 14.0235)):
            Rectangle(2, 18.953)
    extrude(amount=-11.824)

    # Rectangular slot cut through the base for cable or component routing
    plano_base_cut = Plane.XY.offset(0)
    with BuildSketch(plano_base_cut) as s_final:
        with Locations((0, 25)):
            Rectangle(37.039, 3)
    extrude(amount=-12.824, mode=Mode.SUBTRACT)

# Position the top shell on top of the bottom shell
top_shell_positioned = top_shell.part.move(Location((0, 0, bottom_top_z)))

# =============================================================================
# --- D-PAD ---
# =============================================================================
with BuildPart() as dpad_part:
    # Elliptical dome cap at Z=8, extruded 4.5mm upward
    with BuildSketch(Plane.XY.offset(8)):
        Ellipse(16.150, 14.209)
    extrude(amount=4.5)

    # Cross-shaped top face — thin layer at Z=12.5 (2mm tall)
    with Locations((0, 0, 12.5)):
        Box(9.399, 26.400, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(29.399, 9.421, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Cross-shaped body — main structural cross from Z=0 to Z=8
    with Locations((0, 0, 0)):
        Box(9.399, 26.400, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Box(29.399, 9.421, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Horizontal arm loft — tapers the horizontal arm base edge by 0.974mm
    with BuildPart() as horizontal_loft:
        with BuildSketch(Plane.XY) as s1:
            Rectangle(29.399, 9.421)
        with BuildSketch(Plane.XY.offset(-0.974)) as s2:
            Rectangle(27.399, 7.421)
        loft()

    # Vertical arm loft — tapers the vertical arm base edge by 0.974mm
    with BuildPart() as vertical_loft:
        with BuildSketch(Plane.XY) as s1:
            Rectangle(9.399, 26.400)
        with BuildSketch(Plane.XY.offset(-0.974)) as s2:
            Rectangle(7.399, 24.400)
        loft()

# Flip the D-pad upside down and compensate height so base sits at Z=0
dpad_final = dpad_part.part.rotate(Axis.X, 180).move(Location((0, 0, 14.5)))

# Position D-pad inside the controller at the D-pad housing opening (-38, 1)
# Z calculated so the D-pad top aligns flush with the top shell inner face
dpad_z = bottom_top_z - 3 - 14.5 + 3  # = 7.924
dpad_positioned = dpad_final.move(Location((-38, 1, dpad_z)))

# =============================================================================
# --- BUTTONS ---
# =============================================================================
def make_button():
    # Main cylindrical shaft
    with BuildPart() as btn:
        Cylinder(radius=4.8, height=14.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Tapered top surface (truncated cone)
        with Locations((0, 0, 14.5)):
            Cone(bottom_radius=4.8, top_radius=3.8, height=1,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Four lateral guide tabs — one per axis direction
        with Locations((5.315, 0, 0)):
            Box(1.2, 1.8, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-5.315, 0, 0)):
            Box(1.2, 1.8, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 5.315, 0)):
            Box(1.8, 1.2, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, -5.315, 0)):
            Box(1.8, 1.2, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return btn.part

# Button XY positions match the hole locations on the top shell
button_positions = [(28.005, 1), (48.006, 1), (38.006, 9.5), (38.006, -7.5)]

# Base Z calculated so ~3mm of button protrudes above the top shell external face
# and the remaining shaft sits inside the controller body
button_base_z = bottom_top_z - 11.5 + 1  # = 11.924

buttons = []
for pos in button_positions:
    btn = make_button().move(Location((pos[0], pos[1], button_base_z)))
    buttons.append(btn)

# =============================================================================
# --- FINAL ASSEMBLY VIEW ---
# =============================================================================
show(
    bottom_shell.part,
    top_shell_positioned,
    dpad_positioned,
    *buttons,
    names=["Bottom Shell", "Top Shell", "D-Pad", "Button A", "Button B", "Button X", "Button Y"],
    colors=["gray", "lightgray", "orange", "red", "yellow", "blue", "green"],
    alphas=[1.0, 0.6, 1.0, 1.0, 1.0, 1.0, 1.0]
)

print("✅ Assembly complete: Bottom Shell + Top Shell + D-Pad + 4 Buttons")