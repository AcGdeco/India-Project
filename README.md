# RetroPad — Parametric Game Controller

A fully parametric handheld game controller designed and generated entirely in Python using [build123d](https://github.com/gumyr/build123d). All geometry is defined programmatically and exported to STEP format for use in CAD tools such as Autodesk Inventor, Fusion 360, or FreeCAD.

---

## 📁 Project Structure

```
retropad/
├── assembly.py                  # Full assembly — all parts positioned together
├── bottom_shell.py              # Bottom enclosure shell
├── top_shell.py                 # Top enclosure shell
├── button.py                    # Action button (A, B, X, Y)
├── dpad.py                      # Directional pad (D-Pad)
├── validador.py                 # Geometric identity validator
├── RetroPad - Bottom Shell.stl  # Reference STL for bottom shell validation
├── RetroPad - Top Shell.stl     # Reference STL for top shell validation
├── RetroPad - Button.stl        # Reference STL for button validation
├── RetroPad - D-Pad.stl         # Reference STL for D-pad validation
└── README.md
```

---

## 🧩 Parts Overview

### Bottom Shell (`bottom_shell.py`)
The lower half of the controller body.

- Lofted base (Z=0 → Z=3) transitioning from a smaller to a larger chamfered rectangle
- Two hollow vertical walls with a 1mm internal step ledge for the top shell to seat onto
- Five internal support pillars (solid base + thin pin) for PCB/screen mounting
- Two hollow elliptical collars for component alignment
- Rectangular slot for internal cable or component routing

### Top Shell (`top_shell.py`)
The upper half of the controller body, oriented face-down (grows in -Z).

- Mirrored loft base matching the bottom shell profile
- Single-thickness hollow enclosure wall
- Cross-shaped D-pad cutout with elliptical housing collar
- Four action button holes with recessed cylindrical walls and cross-shaped guide slots
- Five hollow mounting pillars aligning with bottom shell pins
- Internal reinforcement ribs for structural stiffness
- Rectangular slot for cable routing

### Action Button (`button.py`)
Shared geometry used for all four action buttons (A, B, X, Y).

- Main cylindrical shaft (radius 4.8mm, height 14.5mm)
- Tapered top surface (truncated cone, 1mm height)
- Four lateral guide tabs (one per axis) for alignment inside the shell guide slots

### D-Pad (`dpad.py`)
Directional pad with cross-shaped geometry.

- Elliptical dome cap
- Cross-shaped body with tapered loft base edges (horizontal and vertical arms)
- Thin top face layer
- Final geometry flipped 180° on the X axis and repositioned so the base sits at Z=0

---

## ⚙️ Assembly (`assembly.py`)

All parts are instantiated and positioned relative to `bottom_top_z`, the Z coordinate where the top shell seats onto the bottom shell.

```
Z = 0               → Bottom shell base (external bottom face)
Z = 3               → Loft top / wall start
Z = 19.424          → Top of bottom shell walls (base assembly height)
Z = bottom_top_z    → Top shell seating plane (with vertical offset adjustments)
```

| Part | Position |
|---|---|
| Bottom Shell | Origin (0, 0, 0) |
| Top Shell | Translated to `bottom_top_z` on Z |
| D-Pad | `(-38, 1, dpad_z)` — inside D-pad housing |
| Button A | `(28.005, 1, button_base_z)` |
| Button B | `(48.006, 1, button_base_z)` |
| Button X | `(38.006, 9.5, button_base_z)` |
| Button Y | `(38.006, -7.5, button_base_z)` |

---

## ✅ Geometric Validation (`validador.py`)

Each part script runs an optional validation against a reference STL file using `check_geometric_identity()`. Instead of slow boolean XOR operations, the validator compares three lightweight metrics:

| Metric | Tolerance | What it detects |
|---|---|---|
| Volume | ≤ 1% difference | Excess or missing material |
| Bounding Box (X, Y, Z) | ≤ 0.5mm per axis | Wrong overall dimensions |
| Surface Area | ≤ 2% difference | Missing or extra faces |

The 2% surface area tolerance accounts for the triangular mesh approximation inherent to STL files.

---

## 🛠️ Requirements

```bash
pip install build123d
pip install ocp-vscode
```

> Recommended editor: **VS Code** with the [OCP CAD Viewer](https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-vscode-viewer) extension for live 3D preview.

---

## 🚀 Usage

Run any individual part to generate and preview it:

```bash
python bottom_shell.py
python top_shell.py
python button.py
python dpad.py
```

Run the full assembly:

```bash
python assembly.py
```

Each script exports a `.step` file to the working directory and optionally validates geometry against the reference STL.

---

## 📐 Coordinate System

All geometry follows a right-handed coordinate system:

- **X** — horizontal axis (left/right)
- **Y** — longitudinal axis (top/bottom of controller)
- **Z** — vertical axis (thickness direction)

The bottom shell grows in **+Z**. The top shell grows in **-Z** and is translated upward in the assembly to sit on top of the bottom shell.

---

## 📄 License

MIT License — free to use, modify, and distribute.
