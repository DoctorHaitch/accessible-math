import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from colorspacious import cspace_convert
from mpl_toolkits.axes_grid1 import SubplotDivider, Size
import json
import os

# Calculate color codes for color vision deficiencies.
def simulate_cvd(colors, deficiency):
    rgb = np.array([mcolors.to_rgb(c) for c in colors])

      # Calculate perceived luminance and convert to grayscale.
    if deficiency == "achromatopsia":
        luminance = 0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]
        return [tuple([l, l, l]) for l in luminance]

      # Use colorspacious library functions to simulate other color vision deficiencies.
    cvd_space = {
        "name": "sRGB1+CVD",
        "cvd_type": deficiency,
        "severity": 100
    }
    simulated = cspace_convert(rgb, cvd_space, "sRGB1")
    simulated = np.clip(simulated, 0, 1)

    return [tuple(c) for c in simulated]


# Builds grids of swatches based on each desired color vision deficiency
# to be simulated.
# Expected input is array of Hex color codes.
# Output is the named .png file with color swatches.
def check_colorblindness(colors, names=None, label=True, outfile="colorblind_check.png"):
    ncol = 3 
    lw = 2
    
    ncolors = len(colors)
    nrow = int(np.ceil(ncolors / ncol))

    conditions = ["Original", "Deutan", "Protan", "Tritan", "Achromatopsia"]

    deutan = simulate_cvd(colors, "deuteranomaly")
    protan = simulate_cvd(colors, "protanomaly")
    tritan = simulate_cvd(colors, "tritanomaly")
    achroma = simulate_cvd(colors, "achromatopsia")

    all_sets = [colors, deutan, protan, tritan, achroma]

    # HARDCODED ABSOLUTE DIMENSIONS (IN INCHES)
    swatch_size = 0.8       # Each individual square color swatch is exactly 0.8 x 0.8 inches
    col_gap = 0.33           # Horizontal whitespace gap between columns of panels
    row_gap = 0.2           # Vertical whitespace gap between rows of panels
    title_height = 0.25     # Allocated top margin space for panel titles
    
    # Mathematical Grid Properties
    panel_width = ncol * swatch_size
    panel_height = nrow * swatch_size

    # Calculate overall figure footprint based on internal geometry
    # Width: Left panel + gap + right panel
    fig_width = panel_width + col_gap + panel_width
    # Height: 3 rows of panels + 3 title areas + gaps between rows
    fig_height = (panel_height * 3) + (title_height * 3) + (row_gap * 2)

    # Base Padding Margins (Outer window bounds in inches)
    margin_left = 0.2
    margin_bottom = 0.2
    fig_width += margin_left * 2
    fig_height += margin_bottom * 2

    # Instantiate the figure with calculated proportions
    fig = plt.figure(figsize=(fig_width, fig_height))

    for idx, cond in enumerate(conditions):
        color_set = all_sets[idx]
        
        # Calculate row and column index of the 3x2 grid layout
        grid_row = idx // 2   # 0 (Top), 1 (Middle), 2 (Bottom)
        grid_col = idx % 2    # 0 (Left), 1 (Right)

        # Precise anchoring math using SubplotDivider sizing blocks
        # Horizontals: Margin -> (Optional: Panel 1 + Gap) -> Active Panel Area
        if grid_col == 0:
            horiz_sizes = [Size.Fixed(margin_left), Size.Fixed(panel_width)]
        else:
            horiz_sizes = [Size.Fixed(margin_left + panel_width + col_gap), Size.Fixed(panel_width)]
            
        # Verticals: Stack upward from the canvas floor
        # Accounts for the flipped visual row ordering (0 is top row graphically)
        bottom_offset = margin_bottom
        if grid_row == 1: # Middle row
            bottom_offset += panel_height + row_gap + title_height
        elif grid_row == 0: # Top row
            bottom_offset += (panel_height * 2) + (row_gap * 2) + (title_height * 2)

        vert_sizes = [Size.Fixed(bottom_offset), Size.Fixed(panel_height)]

        # Lock the axis into this precise dimension matrix
        divider = SubplotDivider(fig, 1, 1, 1, horizontal=horiz_sizes, vertical=vert_sizes)
        ax = fig.add_subplot(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

        # Position title directly relative to the hardcoded block window
        ax.set_title(cond, fontsize=12, fontweight='bold', pad=8)
        
        # Build individual color patches
        for i, color in enumerate(color_set):
            x = i % ncol
            y = i // ncol

            rect = plt.Rectangle((x, y), 1, 1, facecolor=color, linewidth=0)
            ax.add_patch(rect)

            if label and cond == "Original":
                r, g, b = mcolors.to_rgb(color)
                luminance = 0.299 * r + 0.587 * g + 0.114 * b
                text_color = "black" if luminance > 0.4 else "white"

                # Main HEX label (centered)
                ax.text(
                    x + 0.5, y + 0.45, str(color).upper(),
                    ha='center', va='center',
                    color=text_color,
                    fontsize=9,
                    fontweight='bold'
                )

                # Optional name label (bottom, smaller)
                if names is not None and i < len(names):
                    ax.text(
                        x + 0.5, y + 0.8,
                        names[i],
                        ha='center', va='center',
                        color=text_color,
                        fontsize=6,
                        alpha=0.7
                    )
        
        # Layout border grids
        for r in range(nrow + 1):
            if r == nrow:
                remaining_items = ncolors % ncol
                max_x = ncol if remaining_items == 0 else remaining_items
            else:
                max_x = ncol
            if max_x > 0:
                ax.hlines(r, 0, max_x, colors='black', linewidth=lw, capstyle='projecting')

        for c in range(ncol + 1):
            full_rows = ncolors // ncol
            remaining_items = ncolors % ncol
            
            if c <= remaining_items:
                max_y = nrow
            else:
                max_y = full_rows
                
            if max_y > 0:
                ax.vlines(c, 0, max_y, colors='black', linewidth=lw, capstyle='projecting')

        ax.set_xlim(-0.01, ncol + 0.01)
        ax.set_ylim(-0.01, nrow + 0.01)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')
    
    # Save the absolute canvas footprint without shifting layout elements
    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    print(f"Saved image to: {outfile}")
    plt.close()

def shorten_name(name, max_len=18):
    drop_prefixes = ["MSU", "Maverick", "Muted"]

    words = name.split()

    # Remove known prefixes
    while words and words[0] in drop_prefixes:
        words.pop(0)

    if not words:
        words = name.split()

    # Build string word-by-word without exceeding max_len
    result = ""
    for word in words:
        candidate = f"{result} {word}".strip()
        if len(candidate) > max_len:
            break
        result = candidate

    # If nothing fit (rare case), fallback to truncation
    if not result:
        return name[:max_len - 3] + "..."

    # If truncated (didn't include all words), add ellipsis
    if result != " ".join(words):
        result += "..."

    return result

def generate_all_palettes_from_json(json_file, output_dir="."):
    with open(json_file, "r") as f:
        data = json.load(f)

    palettes = data["palettes"]

    for palette in palettes:
        palette_name = palette["palette"]

        # Skip if not changed (default = True if missing)
        if not palette.get("changed", True):
            print(f"Skipping (unchanged): {palette_name}")
            continue

        colors = [c["color"] for c in palette["colors"]]
        names = [shorten_name(c["name"]) for c in palette["colors"]]

        # Clean filename (just in case)
        safe_name = palette_name.lower().replace(" ", "-")

        outfile = os.path.join(output_dir, f"{safe_name}-palette.png")

        print(f"Generating: {outfile}")
        check_colorblindness(colors, names=names, outfile=outfile)

        # Mark as processed
        palette["changed"] = False

    # Save updated JSON back to file
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)


### Example Usage for single palette:
# okabeitopalette=["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"]
# check_colorblindness(okabeitopalette, outfile="okabe-ito-palette.png")

### Usage for loading multiple palettes from a JSON file:
generate_all_palettes_from_json("palettes.json")