import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

# ============================
# Anniversary Check-in Map Generator
# ============================
# This script creates a tech-style check-in map (PNG) with
# 1) A dark grid background
# 2) Five activity locations
# 3) A reserved stamp area (盖章区)
# ----------------------------------
# Output: checkin_map.png in the same directory
# ----------------------------------


def draw_checkin_map(output_path: str = "checkin_map.png"):
    """Generate the anniversary check-in map and save to *output_path*."""

    # Figure setup (A4 ratio ~ 11.69 x 8.27 inches)
    fig, ax = plt.subplots(figsize=(11.69, 8.27), dpi=300)

    # Tech-style color palette
    bg_color = "#0B0D14"       # Deep navy background
    grid_color = "#1F2933"     # Subtle grid lines
    accent = "#08F7FE"         # Neon cyan accents
    danger = "#F50157"         # Magenta-red highlight (stamp area)

    # Apply background color
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Draw grid (10x10)
    for x in range(0, 101, 10):
        ax.axvline(x=x, color=grid_color, linewidth=0.3, zorder=0)
    for y in range(0, 101, 10):
        ax.axhline(y=y, color=grid_color, linewidth=0.3, zorder=0)

    # Activity locations & coordinates (0-100 virtual canvas)
    locations = {
        "粘币游戏": (10, 90),
        "淘趣循环市集": (80, 85),
        "框住时光·与你同行": (20, 50),
        "快问快答": (70, 40),
        "量子纠缠瓶": (40, 10),
    }

    # Draw nodes and labels
    for name, (x, y) in locations.items():
        ax.add_patch(Circle((x, y), 3, facecolor=accent, edgecolor="white", linewidth=0.8, zorder=3))
        ax.text(
            x,
            y - 5,
            name,
            color="white",
            fontsize=9,
            ha="center",
            va="top",
            zorder=4,
        )

    # Connect nodes with dashed path in visiting order
    path_order = [
        "粘币游戏",
        "淘趣循环市集",
        "框住时光·与你同行",
        "快问快答",
        "量子纠缠瓶",
    ]
    for i in range(len(path_order) - 1):
        x1, y1 = locations[path_order[i]]
        x2, y2 = locations[path_order[i + 1]]
        ax.plot(
            [x1, x2],
            [y1, y2],
            color=accent,
            linewidth=0.6,
            linestyle="--",
            zorder=2,
        )

    # Reserved stamp area (bottom-right)
    stamp_rect = Rectangle(
        (80, 0),
        20,
        20,
        linewidth=1.5,
        edgecolor=danger,
        facecolor="none",
        linestyle="--",
        zorder=5,
    )
    ax.add_patch(stamp_rect)
    ax.text(
        90,
        10,
        "盖章区",
        color=danger,
        fontsize=10,
        ha="center",
        va="center",
        zorder=6,
    )

    # Final plot aesthetics
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    plt.tight_layout()

    # Save the image (include figure facecolor)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    draw_checkin_map()