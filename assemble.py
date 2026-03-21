from build123d import *
from ocp_vscode import show

# =============================================================================
# --- BOTTOM SHELL ---
# =============================================================================
with BuildPart() as bottom_shell:
    base_plane = Plane.XY
    loft_top_plane = Plane.XY.offset(3)

    with BuildSketch(base_plane) as s1:
        r1 = Rectangle(129, 47)
        chamfer(r1.vertices(), length=8.671)
    with BuildSketch(loft_top_plane) as s2:
        r2 = Rectangle(135, 53)
        chamfer(r2.vertices(), length=10.429)
    loft()

    height_1 = 6.6
    wall1_top_plane = Plane.XY.offset(3 + height_1)
    with BuildSketch(loft_top_plane) as sk1:
        Rectangle(135, 53)
        chamfer(vertices(), length=10.429)
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 4, 53 - 4)
            chamfer(vertices(), length=9.258)
    extrude(amount=height_1)

    with BuildSketch(wall1_top_plane) as sk2:
        Rectangle(135 - 2, 53 - 2)
        chamfer(vertices(), length=9.845)
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 4, 53 - 4)
            chamfer(vertices(), length=9.258)
    extrude(amount=9.824)

    with Locations((52.5, 13.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((52.5, 13.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, 13.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, 13.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((52.5, -11.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((52.5, -11.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, -11.5, 3)):
        Cylinder(radius=2.5, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((-52.5, -11.5, 6)):
        Cylinder(radius=1, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, -11.5, 3)):
        Cylinder(radius=4, height=3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, -11.5, 6)):
        Cylinder(radius=2.5, height=13.424, align=(Align.CENTER, Align.CENTER, Align.MIN))

    ellipse_plane = Plane.XY.offset(3)
    with BuildSketch(ellipse_plane) as s_elipse1:
        with Locations((38, 1)):
            Ellipse(10.5, 9)
            with BuildSketch(mode=Mode.SUBTRACT):
                with Locations((38, 1)):
                    Ellipse(9.5, 8)
    extrude(amount=3)
    with BuildSketch(ellipse_plane) as s_elipse2:
        with Locations((-38, 1)):
            Ellipse(10.5, 9)
            with BuildSketch(mode=Mode.SUBTRACT):
                with Locations((-38, 1)):
                    Ellipse(9.5, 8)
    extrude(amount=3)

    slot_plane = Plane.XY.offset(4.6)
    with BuildSketch(slot_plane, mode=Mode.SUBTRACT) as s_cut:
        with Locations((0, 25.5)):
            Rectangle(37.039, 2)
    extrude(amount=14.824, mode=Mode.SUBTRACT)

# Topo da bottom shell (+2mm acumulado da sessão anterior, +2mm novo = +4mm total)
bottom_top_z = 3 + 6.6 + 9.824 + 2 + 1  # = 22.424

# =============================================================================
# --- TOP SHELL ---
# =============================================================================
with BuildPart() as top_shell:
    plano_base = Plane.XY
    plano_topo_loft = Plane.XY.offset(-3)

    with BuildSketch(plano_base) as s1:
        r1 = Rectangle(129, 47)
        chamfer(r1.vertices(), length=8.671)
    with BuildSketch(plano_topo_loft) as s2:
        r2 = Rectangle(135, 53)
        chamfer(r2.vertices(), length=10.429)
    loft()

    altura_1 = 9.824
    with BuildSketch(plano_topo_loft) as sk1:
        Rectangle(135, 53)
        chamfer(vertices(), length=10.429)
        with BuildSketch(mode=Mode.SUBTRACT):
            Rectangle(135 - 2, 53 - 2)
            chamfer(vertices(), length=9.844)
    extrude(amount=-altura_1)

    plano_rasgo = Plane.XY.offset(0)
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte:
        with Locations((-38, 1)):
            Rectangle(29.999, 10.021)
    extrude(amount=-3, mode=Mode.SUBTRACT)
    with BuildSketch(plano_rasgo, mode=Mode.SUBTRACT) as s_corte2:
        with Locations((-38, 1)):
            Rectangle(10.021, 26.999)
    extrude(amount=-3, mode=Mode.SUBTRACT)

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

    with Locations((-52.499, 13.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((-52.499, 13.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((-52.499, -11.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((-52.499, -11.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((0, -11.5, -3)):
        Cylinder(radius=4, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((0, -11.5, -3)):
        Cylinder(radius=2.6, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((52.499, 13.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((52.499, 13.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    with Locations((52.499, -11.5, -3)):
        Cylinder(radius=2.5, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX))
    with Locations((52.499, -11.5, -3)):
        Cylinder(radius=1.1, height=11.824, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)

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

    plano_internal = Plane.XY.offset(-3)
    with BuildSketch(plano_internal) as s_wall1:
        with Locations((0, 3.547)):
            Rectangle(35.239, 2)
    extrude(amount=-11.824)
    with BuildSketch(plano_internal) as s_wall2:
        with Locations((-16.6195, 14.0235)):
            Rectangle(2, 18.953)
        with Locations((16.6195, 14.0235)):
            Rectangle(2, 18.953)
    extrude(amount=-11.824)

    plano_base_cut = Plane.XY.offset(0)
    with BuildSketch(plano_base_cut) as s_final:
        with Locations((0, 25)):
            Rectangle(37.039, 3)
    extrude(amount=-12.824, mode=Mode.SUBTRACT)

top_shell_positioned = top_shell.part.move(Location((0, 0, bottom_top_z)))

# =============================================================================
# --- D-PAD ---
# =============================================================================
with BuildPart() as dpad_part:
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
        with BuildSketch(Plane.XY) as s1:
            Rectangle(29.399, 9.421)
        with BuildSketch(Plane.XY.offset(-0.974)) as s2:
            Rectangle(27.399, 7.421)
        loft()

    with BuildPart() as vertical_loft:
        with BuildSketch(Plane.XY) as s1:
            Rectangle(9.399, 26.400)
        with BuildSketch(Plane.XY.offset(-0.974)) as s2:
            Rectangle(7.399, 24.400)
        loft()

dpad_final = dpad_part.part.rotate(Axis.X, 180).move(Location((0, 0, 14.5)))

# D-pad: +2mm anterior + 2.5mm novo = +4.5mm total sobre o cálculo base
dpad_z = bottom_top_z - 3 - 14.5 + 3  # = 10.424
dpad_positioned = dpad_final.move(Location((-38, 1, dpad_z)))

# =============================================================================
# --- BUTTONS ---
# =============================================================================
def make_button():
    with BuildPart() as btn:
        Cylinder(radius=4.8, height=14.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 0, 14.5)):
            Cone(bottom_radius=4.8, top_radius=3.8, height=1,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((5.315, 0, 0)):
            Box(1.2, 1.8, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((-5.315, 0, 0)):
            Box(1.2, 1.8, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, 5.315, 0)):
            Box(1.8, 1.2, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations((0, -5.315, 0)):
            Box(1.8, 1.2, 5.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return btn.part

button_positions = [(28.005, 1), (48.006, 1), (38.006, 9.5), (38.006, -7.5)]

# Botões: +2mm anterior + 1mm novo (base sobe = menos exposto) = +3mm total
button_base_z = bottom_top_z - 11.5 + 1  # = 14.924

buttons = []
for pos in button_positions:
    btn = make_button().move(Location((pos[0], pos[1], button_base_z)))
    buttons.append(btn)

# =============================================================================
# --- VISUALIZAÇÃO FINAL ---
# =============================================================================
show(
    bottom_shell.part,
    top_shell_positioned,
    dpad_positioned,
    *buttons,
    names=["Bottom Shell", "Top Shell", "D-Pad", "Botão A", "Botão B", "Botão X", "Botão Y"],
    colors=["gray", "lightgray", "orange", "red", "yellow", "blue", "green"],
    alphas=[1.0, 0.6, 1.0, 1.0, 1.0, 1.0, 1.0]
)

print("✅ Assembly completo: Bottom Shell + Top Shell + D-Pad + 4 Botões")