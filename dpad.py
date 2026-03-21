from build123d import *
from ocp_vscode import show
from validador import check_geometric_identity

# --- ORIGINAL GEOMETRY (NO DIMENSION CHANGES) ---
with BuildPart() as dpad:
    # Elliptical dome cap — sits at Z=8, extruded 4.5mm upward
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

    # Horizontal arm loft — tapers the horizontal arm base edge by 0.974mm downward
    with BuildPart() as horizontal_loft:
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974)
        with BuildSketch(base_plane) as s1:
            Rectangle(29.399, 9.421)
        with BuildSketch(top_plane) as s2:
            Rectangle(27.399, 7.421)
        loft()
        horizontal_loft.part.move(Location((0, 0, 0)))

    # Vertical arm loft — tapers the vertical arm base edge by 0.974mm downward
    with BuildPart() as vertical_loft:
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974)
        with BuildSketch(base_plane) as s1:
            Rectangle(9.399, 26.400)
        with BuildSketch(top_plane) as s2:
            Rectangle(7.399, 24.400)
        loft()
        vertical_loft.part.move(Location((0, 0, 0)))

# --- FINAL ORIENTATION & POSITION ---

# 1. Extract the final solid from the BuildPart context
final_part = dpad.part

# 2. Rotate 180 degrees around the X axis to flip the D-pad upside down
# 3. Translate upward by 14.5mm to compensate — the former top becomes the new base at Z=0
dpad_inverted = final_part.rotate(Axis.X, 180).move(Location((0, 0, 14.5)))

# Visualize the flipped D-pad in the OCP viewer
show(dpad_inverted)

# Validate geometry against the reference STL
result = check_geometric_identity(dpad_inverted, "RetroPad - D-Pad.stl")