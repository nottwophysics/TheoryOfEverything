"""
Maya Visualizer — Interactive Visual Models of Advaita Concepts

Visualizations:
1. Unity → Multiplicity → Unity (Maya unfolding and folding back)
2. Rope-Snake superimposition at varying ignorance levels
3. Guna dynamics over time
4. Neti-Neti layer stripping
5. Three levels of reality
6. Fractal self-similarity (non-duality in structure)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from brahman.consciousness import Brahman
from maya.superimposition import Adhyasa
from maya.gunas import Gunas, GunaBalance
from maya.nama_rupa import NamaRupa
from emergence.spacetime import ConsciousnessField


# Custom colormap: from unity (gold) to multiplicity (rainbow)
UNITY_CMAP = LinearSegmentedColormap.from_list(
    "unity", ["#FFD700", "#FF6B35", "#E91E63", "#9C27B0", "#3F51B5", "#00BCD4"]
)


class MayaVisualizer:
    """Interactive visualizations of Advaita Vedanta concepts."""

    def __init__(self, save_dir: str = None):
        self.save_dir = save_dir or os.path.join(os.path.dirname(__file__), "..", "output")
        os.makedirs(self.save_dir, exist_ok=True)
        self.brahman = Brahman()

    def plot_unity_to_multiplicity(self, steps: int = 6):
        """
        Watch Brahman appear to become the world through Maya.

        Starts with undifferentiated unity.
        Each step adds more apparent differentiation.
        Final step: dissolve back to unity.
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(
            "Unity → Multiplicity → Unity\n"
            "(Brahman → World through Maya → Back to Brahman)",
            fontsize=14, fontweight="bold",
        )

        field = self.brahman.field
        n = len(field)
        x = np.linspace(0, 1, n)

        for idx, ax in enumerate(axes.flat):
            if idx < steps - 1:
                # Increasing differentiation (Maya deepening)
                depth = idx
                frequencies = [2 ** i for i in range(1, depth + 2)]
                modulated = np.real(field.copy())
                for freq in frequencies:
                    modulated += 0.15 * np.sin(2 * np.pi * freq * x + idx)

                ax.fill_between(x, modulated, alpha=0.7, color=UNITY_CMAP(idx / steps))
                ax.plot(x, modulated, color="black", linewidth=0.5)
                ax.set_title(f"Maya Depth: {depth}\n({'Unity' if depth == 0 else f'{len(frequencies)} apparent forms'})")
            else:
                # Return to unity
                unity = np.real(field)
                ax.fill_between(x, unity, alpha=0.9, color="#FFD700")
                ax.plot(x, unity, color="black", linewidth=0.5)
                ax.set_title("Moksha: Return to Unity\n(Brahman — One Without a Second)")

            ax.set_ylim(-0.5, 0.5)
            ax.set_xlabel("Field")
            ax.set_ylabel("Amplitude")

        plt.tight_layout()
        path = os.path.join(self.save_dir, "unity_to_multiplicity.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_rope_snake(self):
        """
        Visualize the rope-snake superimposition at different ignorance levels.

        As ignorance decreases, the 'snake' gradually becomes the 'rope'.
        """
        adhyasa = Adhyasa()
        rope = np.sin(np.linspace(0, 2 * np.pi, 256)) * 0.3 + 0.5

        ignorance_levels = [0.95, 0.75, 0.55, 0.35, 0.15, 0.05]
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(
            "Adhyasa (Superimposition): Rope → Snake → Rope\n"
            "As ignorance decreases, the snake 'becomes' the rope",
            fontsize=14, fontweight="bold",
        )

        for ax, ign in zip(axes.flat, ignorance_levels):
            result = adhyasa.superimpose(rope, ign, "snake")
            apparent = np.real(result.apparent)

            ax.plot(apparent, color="red" if ign > 0.5 else "green", linewidth=1.5, label="Perceived")
            ax.plot(rope, color="brown", linewidth=1, linestyle="--", alpha=0.5, label="Actual (rope)")
            ax.fill_between(range(len(apparent)), apparent, rope, alpha=0.2,
                          color="red" if ign > 0.5 else "green")

            sees = "SNAKE" if ign > 0.7 else ("???" if ign > 0.3 else "ROPE")
            ax.set_title(f"Ignorance: {ign:.0%} — Sees: {sees}")
            ax.legend(fontsize=8)
            ax.set_ylim(-1, 2)

        plt.tight_layout()
        path = os.path.join(self.save_dir, "rope_snake.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_guna_dynamics(self, steps: int = 200):
        """
        Visualize the cycling of Sattva, Rajas, and Tamas over time.

        Shows how experiential quality shifts continuously while
        the underlying substrate (Brahman) remains unchanged.
        """
        gunas = Gunas(GunaBalance(0.4, 0.35, 0.25))
        history = gunas.simulate_cycle(steps)

        sattva = [h["sattva"] for h in history]
        rajas = [h["rajas"] for h in history]
        tamas = [h["tamas"] for h in history]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle(
            "Guna Dynamics — The Ever-Changing Qualities of Experience\n"
            "(Brahman is Nirguna — beyond all Gunas)",
            fontsize=14, fontweight="bold",
        )

        # Line plot
        t = range(steps)
        ax1.plot(t, sattva, color="#4CAF50", linewidth=2, label="Sattva (Clarity)")
        ax1.plot(t, rajas, color="#FF5722", linewidth=2, label="Rajas (Activity)")
        ax1.plot(t, tamas, color="#607D8B", linewidth=2, label="Tamas (Inertia)")
        ax1.axhline(y=1/3, color="gold", linestyle=":", alpha=0.5, label="Balance point")
        ax1.set_ylabel("Proportion")
        ax1.set_xlabel("Time")
        ax1.legend()
        ax1.set_title("Guna Proportions Over Time")

        # Stacked area
        ax2.stackplot(
            t, sattva, rajas, tamas,
            colors=["#4CAF50", "#FF5722", "#607D8B"],
            labels=["Sattva", "Rajas", "Tamas"],
            alpha=0.8,
        )
        ax2.set_ylabel("Proportion")
        ax2.set_xlabel("Time")
        ax2.legend(loc="upper right")
        ax2.set_title("Guna Composition (always sums to 1.0 — only proportions change)")

        plt.tight_layout()
        path = os.path.join(self.save_dir, "guna_dynamics.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_neti_neti(self):
        """
        Visualize the Neti-Neti process — stripping away layers
        to reveal the witness.
        """
        from liberation.neti_neti import NetiNeti

        inquiry = NetiNeti(field_size=256)
        result = inquiry.inquire(verbose=False)
        process = result["process"]

        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        fig.suptitle(
            "Neti Neti — 'Not This, Not This'\n"
            "Stripping away layers of false identification",
            fontsize=14, fontweight="bold",
        )

        # Build cumulative field
        layers = inquiry._build_default_layers()
        total = np.zeros(256)
        for layer in layers:
            total += layer.content

        remainder = total.copy()
        for idx, (ax, layer) in enumerate(zip(axes.flat, layers)):
            # Show the layer being removed
            ax.fill_between(range(256), layer.content, alpha=0.3, color="red", label="Negated")
            ax.plot(remainder, color="blue", linewidth=1, label="Remainder")
            remainder = remainder - layer.content
            ax.plot(remainder, color="green", linewidth=1, linestyle="--", label="After Neti")

            ax.set_title(f"Neti: {layer.name}\n(attachment: {layer.attachment_strength:.0%})", fontsize=9)
            ax.set_ylim(-5, 8)
            if idx == 0:
                ax.legend(fontsize=7)

        plt.tight_layout()
        path = os.path.join(self.save_dir, "neti_neti.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_three_levels(self):
        """
        Visualize the three levels of reality side by side.
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(
            "Three Levels of Reality (Satta Traividhya)",
            fontsize=14, fontweight="bold",
        )

        n = 256
        x = np.linspace(0, 1, n)

        # Paramarthika — pure, undifferentiated
        field = np.ones(n) / np.sqrt(n)
        axes[0].fill_between(x, np.real(field), alpha=0.9, color="#FFD700")
        axes[0].set_title("Paramarthika (Absolute)\nBrahman — One Without a Second")
        axes[0].set_ylabel("Reality")
        axes[0].annotate("Never sublated", xy=(0.5, 0.03), ha="center", fontsize=10,
                        fontweight="bold", color="darkgoldenrod")

        # Vyavaharika — structured, multiple forms
        empirical = np.real(field) + 0.02 * np.sin(8 * np.pi * x) + 0.01 * np.sin(20 * np.pi * x)
        axes[1].plot(x, empirical, color="#2196F3", linewidth=1.5)
        axes[1].fill_between(x, empirical, alpha=0.5, color="#2196F3")
        axes[1].set_title("Vyavaharika (Empirical)\nThe World of Experience")
        axes[1].annotate("Sublated by Self-knowledge", xy=(0.5, 0.005), ha="center",
                        fontsize=9, color="navy")

        # Pratibhasika — noisy, erroneous
        np.random.seed(42)
        illusory = np.real(field) + np.random.randn(n) * 0.03
        axes[2].plot(x, illusory, color="#F44336", linewidth=0.8, alpha=0.7)
        axes[2].fill_between(x, illusory, alpha=0.3, color="#F44336")
        axes[2].set_title("Pratibhasika (Illusory)\nDream / Error / Mirage")
        axes[2].annotate("Sublated upon waking", xy=(0.5, 0.005), ha="center",
                        fontsize=9, color="darkred")

        for ax in axes:
            ax.set_xlabel("Field")
            ax.set_ylim(-0.05, 0.15)

        plt.tight_layout()
        path = os.path.join(self.save_dir, "three_levels.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_fractal_unity(self, depth: int = 5):
        """
        Fractal self-similarity as a model of non-duality.

        Zoom into any part of a fractal → same structure.
        This mirrors Advaita: look at any part of reality → Brahman.
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(
            "Fractal Unity — Self-Similarity as Non-Duality\n"
            "Every part contains the whole. Every entity IS Brahman.",
            fontsize=14, fontweight="bold",
        )

        # Generate Mandelbrot-like fractal
        for idx, ax in enumerate(axes.flat):
            zoom = 2.0 ** idx
            cx = -0.7 + 0.1 / zoom
            cy = 0.27015 + 0.05 / zoom
            span = 2.0 / zoom

            x_range = np.linspace(cx - span, cx + span, 400)
            y_range = np.linspace(cy - span, cy + span, 400)
            X, Y = np.meshgrid(x_range, y_range)
            C = X + 1j * Y

            Z = np.zeros_like(C)
            M = np.zeros(C.shape, dtype=float)

            for i in range(100):
                mask = np.abs(Z) <= 2
                Z[mask] = Z[mask] ** 2 + C[mask]
                M[mask] = i

            ax.imshow(M, extent=[cx - span, cx + span, cy - span, cy + span],
                     cmap=UNITY_CMAP, aspect="equal")
            ax.set_title(f"Zoom: {zoom:.0f}x\n{'Whole' if idx == 0 else 'Same pattern at every scale'}")
            ax.set_xticks([])
            ax.set_yticks([])

        plt.tight_layout()
        path = os.path.join(self.save_dir, "fractal_unity.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_emergent_spacetime(self):
        """
        Visualize how space emerges from consciousness differentiation.
        """
        cf = ConsciousnessField(resolution=64)

        fig, axes = plt.subplots(1, 4, figsize=(16, 4))
        fig.suptitle(
            "Emergent Spacetime — Dimensions Arise from Self-Reference",
            fontsize=14, fontweight="bold",
        )

        # Step 0: Undifferentiated
        axes[0].bar([0], [1], color="#FFD700", width=0.5)
        axes[0].set_title("0 Dimensions\n(Pure Awareness)")
        axes[0].set_ylabel("Awareness")
        axes[0].set_xlim(-1, 1)

        # Steps 1-3: Increasing differentiation
        for d in range(1, 4):
            cf_step = ConsciousnessField(resolution=64)
            field = cf_step.differentiate(d)
            axes[d].plot(np.real(field), color=UNITY_CMAP(d / 4), linewidth=1.5)
            axes[d].fill_between(range(len(field)), np.real(field), alpha=0.3,
                               color=UNITY_CMAP(d / 4))
            axes[d].set_title(f"{d} Dimension{'s' if d > 1 else ''}\n(Self-reference depth: {d})")

        for ax in axes:
            ax.set_xlabel("Field")

        plt.tight_layout()
        path = os.path.join(self.save_dir, "emergent_spacetime.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def generate_all(self) -> list:
        """Generate all visualizations and return their file paths."""
        paths = []
        visualizations = [
            ("Unity to Multiplicity", self.plot_unity_to_multiplicity),
            ("Rope-Snake Superimposition", self.plot_rope_snake),
            ("Guna Dynamics", self.plot_guna_dynamics),
            ("Neti Neti Process", self.plot_neti_neti),
            ("Three Levels of Reality", self.plot_three_levels),
            ("Fractal Unity", self.plot_fractal_unity),
            ("Emergent Spacetime", self.plot_emergent_spacetime),
        ]

        for name, func in visualizations:
            try:
                path = func()
                paths.append({"name": name, "path": path, "status": "success"})
                print(f"  Generated: {name}")
            except Exception as e:
                paths.append({"name": name, "error": str(e), "status": "failed"})
                print(f"  Failed: {name} — {e}")

        return paths
