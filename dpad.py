from build123d import *
from ocp_vscode import show

# Creating a part with a main body, cross-sections, and lofted trunks
with BuildPart() as dpad:
    
    # --- 1. MAIN ELLIPTICAL BASE ---
    # Define the primary elliptical sketch (X and Y semi-axes)
    with BuildSketch():
        Ellipse(16.150, 14.209)

    # Extrude the elliptical base upwards by 4.5mm
    extrude(amount=4.5)

    # --- 2. TOP CROSS STRUCTURE (D-PAD SHAPE) ---
    # Vertical bar of the cross, starting at Z=4.5
    with Locations((0, 0, 4.5)):
        Box(
            9.399,
            26.400, 
            2, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # Horizontal bar of the cross, starting at Z=4.5
    with Locations((0, 0, 4.5)):
        Box(
            29.399, 
            9.421,
            2, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # --- 3. BOTTOM SUPPORT STRUCTURE ---
    # Vertical bottom support starting at Z=-4.5
    with Locations((0, 0, -4.5)):
        Box(
            9.399, 
            26.400,
            8, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # Horizontal bottom support starting at Z=-4.5
    with Locations((0, 0, -4.5)):
        Box(
            29.399, 
            9.421,
            8, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    # --- 4. TAPERED LOFT (HORIZONTAL TRUNK) ---
    with BuildPart() as horizontal_loft:
        # Define the two profiles (slices) for the lofted trunk
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974) # Set height offset

        # Sketch the base rectangle (larger)
        with BuildSketch(base_plane) as s1:
            Rectangle(29.399, 9.421)
        
        # Sketch the top rectangle (smaller for tapering)
        with BuildSketch(top_plane) as s2:
            Rectangle(27.399, 7.421)

        # Connect the two sketches using the Loft command
        loft()

        # Position the lofted part at the specific project height
        horizontal_loft.part.move(Location((0, 0, -4.5)))

    # --- 5. TAPERED LOFT (VERTICAL TRUNK) ---
    with BuildPart() as vertical_loft:
        # Define the base and top planes
        base_plane = Plane.XY
        top_plane = Plane.XY.offset(-0.974)

        # Sketch the vertical base rectangle
        with BuildSketch(base_plane) as s1:
            Rectangle(9.399, 26.400)
        
        # Sketch the tapered vertical top rectangle
        with BuildSketch(top_plane) as s2:
            Rectangle(7.399, 24.400)

        # Create the lofted solid
        loft()

        # Position the vertical lofted part
        vertical_loft.part.move(Location((0, 0, -4.5)))
    
# Send the final part to the VS Code side panel for visualization
show(dpad)