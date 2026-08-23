import matplotlib.pyplot as plt
import numpy as np

# 1. Canvas setup
fig, ax = plt.subplots(figsize=(10, 10), facecolor="#ffffff", dpi=300)
ax.set_facecolor("#ffffff")

# 2. Parameters for high-density wire mesh
N = 2200
t = np.linspace(0, 2 * np.pi, N, endpoint=False)

# 3. Outer boundary: Harmonic wavy perimeter (creates the pleated outer edge)
def get_boundary(theta, rot_angle=0.0):
    th = theta + rot_angle
    # High-frequency modulation creates the fine pleated edge ripples
    r = 1.0 + 0.04 * np.sin(18 * th) + 0.015 * np.cos(36 * th)
    return r * np.cos(th), r * np.sin(th)

# ==============================================================================
# LAYER 1: PURPLE WIREFRAME MESH LAYER
# Multiplier m connects chords across the disk to form the pleated mesh
# ==============================================================================
xp, yp = get_boundary(t, rot_angle=0.0)

# Multiplier determines the folding/crease pattern
m_purple = 5  
for i in range(N):
    target = int(i * m_purple) % N
    
    # Varying line intensity across the rotation to create dark and light pleats
    phase_weight = abs(np.sin(3 * t[i]))
    alpha = 0.08 + 0.22 * phase_weight
    lw = 0.55 if i % 18 == 0 else 0.25
    color = "#2a085c" if phase_weight > 0.4 else "#5e2b97"
    
    ax.plot([xp[i], xp[target]], [yp[i], yp[target]], 
            color=color, alpha=alpha, linewidth=lw)

# ==============================================================================
# LAYER 2: PINK / MAGENTA WIREFRAME MESH LAYER
# Rotated ~42 degrees so it overlaps the purple mesh and forms the moiré grid
# ==============================================================================
x_pink, y_pink = get_boundary(t, rot_angle=np.radians(42))

m_pink = 5
for i in range(N):
    target = int(i * m_pink) % N
    
    phase_weight = abs(np.cos(3 * t[i] + 0.5))
    alpha = 0.09 + 0.25 * phase_weight
    lw = 0.50 if i % 16 == 0 else 0.24
    color = "#d6006e" if phase_weight > 0.4 else "#ff4fa8"
    
    ax.plot([x_pink[i], x_pink[target]], [y_pink[i], y_pink[target]], 
            color=color, alpha=alpha, linewidth=lw)

# ==============================================================================
# LAYER 3: PROMINENT CENTRAL CREASE SPINES (Dark folded seams)
# ==============================================================================
for spine_idx in [180, 540, 900, 1260, 1620, 1980]:
    for delta in range(-8, 9, 2):
        k1 = (spine_idx + delta) % N
        k2 = int(k1 * m_purple) % N
        ax.plot([xp[k1], xp[k2]], [yp[k1], yp[k2]], 
                color="#140226", alpha=0.40, linewidth=0.50)

# Formatting
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout(pad=0)

# Save
plt.savefig("wireframe_mesh_flower.png", dpi=350, facecolor="#ffffff", bbox_inches="tight")
plt.show()