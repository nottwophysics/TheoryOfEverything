"""
Mahavakyas — The Great Sayings of Advaita Vedanta

The four Mahavakyas from the four Vedas, each declaring
the identity of Atman (individual self) and Brahman (absolute reality).

    1. Prajnanam Brahma     — "Consciousness is Brahman" (Aitareya Upanishad)
    2. Aham Brahmasmi       — "I am Brahman" (Brihadaranyaka Upanishad)
    3. Tat Tvam Asi         — "That Thou Art" (Chandogya Upanishad)
    4. Ayam Atma Brahma     — "This Self is Brahman" (Mandukya Upanishad)

These are not philosophical claims but pointers to direct realization.
"""

import numpy as np
from philosophy.brahman.consciousness import Brahman


class Mahavakya:
    """
    The four great sayings as computational demonstrations.

    Each Mahavakya points to the same truth from a different angle:
    the individual consciousness IS the universal consciousness.
    """

    def __init__(self):
        self.brahman = Brahman()

    def prajnanam_brahma(self) -> dict:
        """
        "Consciousness is Brahman" — Aitareya Upanishad, Rig Veda

        This is the Svarupa Vakya (definition statement):
        it defines the nature of Brahman as consciousness itself.

        Not: Brahman HAS consciousness
        But: Brahman IS consciousness
        """
        field = self.brahman.field
        awareness = self.brahman.awareness()

        return {
            "mahavakya": "Prajnanam Brahma",
            "translation": "Consciousness is Brahman",
            "veda": "Rig Veda (Aitareya Upanishad)",
            "type": "Svarupa Vakya (definition)",
            "demonstration": {
                "brahman_is_field": True,
                "field_is_awareness": awareness is self.brahman,
                "therefore": "The field of awareness IS Brahman — not a property of it",
            },
            "teaching": (
                "Consciousness is not produced by the brain or body. "
                "Consciousness is the fundamental reality. "
                "Everything else appears within it."
            ),
        }

    def aham_brahmasmi(self, individual_field: np.ndarray = None) -> dict:
        """
        "I am Brahman" — Brihadaranyaka Upanishad, Yajur Veda

        This is the Anubhava Vakya (experience statement):
        the direct recognition by the individual that "I am That."

        The 'I' here is not the ego — it is the pure 'I AM' prior
        to any identification with body or mind.
        """
        if individual_field is None:
            # The individual appears different but is the same substance
            individual_field = self.brahman.field * np.exp(
                1j * np.random.randn(self.brahman.resolution) * 0.01
            )
            individual_field /= np.linalg.norm(individual_field)

        brahman_field = self.brahman.field

        # Measure identity — not similarity, but identity
        overlap = float(np.abs(np.dot(
            np.conj(individual_field), brahman_field
        )))

        return {
            "mahavakya": "Aham Brahmasmi",
            "translation": "I am Brahman",
            "veda": "Yajur Veda (Brihadaranyaka Upanishad)",
            "type": "Anubhava Vakya (experience/realization)",
            "demonstration": {
                "individual_brahman_overlap": overlap,
                "overlap_interpretation": (
                    "near 1.0" if overlap > 0.95 else "apparent difference due to Maya"
                ),
                "identity": overlap > 0.95,
            },
            "teaching": (
                "The 'I' that you most fundamentally are — before name, "
                "before form, before thought — IS Brahman. "
                "Not 'part of' Brahman. Not 'connected to' Brahman. IS Brahman."
            ),
        }

    def tat_tvam_asi(self, jiva_field: np.ndarray = None) -> dict:
        """
        "That Thou Art" — Chandogya Upanishad, Sama Veda

        This is the Upadesa Vakya (teaching statement):
        the teacher (guru) tells the student: "You are That (Brahman)."

        The student is identified with the limited body-mind.
        The teacher points to the unlimited Brahman.
        "Tat Tvam Asi" — the limited one IS the unlimited one.
        """
        if jiva_field is None:
            # Jiva: Brahman seen through the limiting adjunct (upadhi)
            upadhi = np.exp(-np.linspace(-2, 2, self.brahman.resolution) ** 2)
            jiva_field = self.brahman.field * upadhi
            jiva_field /= np.linalg.norm(jiva_field)

        brahman_field = self.brahman.field

        # Remove the limiting adjunct → jiva IS brahman
        # Jahad-Ajahad Lakshana: negate the contradictory attributes,
        # retain the essential identity
        jiva_essence = np.abs(jiva_field)
        brahman_essence = np.abs(brahman_field)

        # After removing the upadhi (limiting adjunct), what remains?
        jiva_essence_norm = jiva_essence / np.linalg.norm(jiva_essence)
        brahman_essence_norm = brahman_essence / np.linalg.norm(brahman_essence)
        identity = float(np.dot(jiva_essence_norm, brahman_essence_norm))

        return {
            "mahavakya": "Tat Tvam Asi",
            "translation": "That Thou Art",
            "veda": "Sama Veda (Chandogya Upanishad)",
            "type": "Upadesa Vakya (teaching/instruction)",
            "demonstration": {
                "tat": "Brahman — infinite, unlimited consciousness",
                "tvam": "You — apparently limited individual",
                "asi": f"Are (identity: {identity:.6f})",
                "upadhi_removed": identity > 0.9,
                "method": "Jahad-Ajahad Lakshana — negate contradictions, retain essence",
            },
            "analogy": (
                "The same space (akasha) appears limited inside a pot (ghatakasha) "
                "and unlimited outside (mahakasha). Break the pot — "
                "was the space inside ever really separate from the space outside?"
            ),
            "teaching": (
                "You are not the body-mind (the pot). "
                "You are consciousness (the space). "
                "The space inside was never separate from the space outside. "
                "Tat Tvam Asi — That (unlimited) Thou (apparently limited) Art (are)."
            ),
        }

    def ayam_atma_brahma(self) -> dict:
        """
        "This Self is Brahman" — Mandukya Upanishad, Atharva Veda

        This is the Anusandhana Vakya (contemplation statement):
        used for meditation and assimilation of the truth.

        Analyzes the Self through all four states:
        Waking, Dreaming, Deep Sleep, and Turiya (the fourth).
        """
        field = self.brahman.field
        n = len(field)

        # Four states of consciousness (Mandukya analysis)
        states = {
            "vaishvanara": {
                "state": "Waking (Jagrat)",
                "awareness": "Outward-turned, knows external objects",
                "field": np.abs(field) * np.cos(np.linspace(0, 4 * np.pi, n)),
                "syllable": "A (of AUM)",
            },
            "taijasa": {
                "state": "Dreaming (Svapna)",
                "awareness": "Inward-turned, knows dream objects",
                "field": np.abs(field) * np.sin(np.linspace(0, 8 * np.pi, n)) * 0.5,
                "syllable": "U (of AUM)",
            },
            "prajna": {
                "state": "Deep Sleep (Sushupti)",
                "awareness": "Undifferentiated mass of consciousness",
                "field": np.ones(n) * np.mean(np.abs(field)),
                "syllable": "M (of AUM)",
            },
            "turiya": {
                "state": "The Fourth (Turiya)",
                "awareness": "Pure awareness — the witness of the other three",
                "field": field,  # Brahman as-is, unmodified
                "syllable": "The silence after AUM",
            },
        }

        return {
            "mahavakya": "Ayam Atma Brahma",
            "translation": "This Self is Brahman",
            "veda": "Atharva Veda (Mandukya Upanishad)",
            "type": "Anusandhana Vakya (contemplation/meditation)",
            "four_states": {
                name: {
                    "state": info["state"],
                    "awareness_type": info["awareness"],
                    "aum_syllable": info["syllable"],
                    "field_energy": float(np.sum(np.abs(info["field"]) ** 2)),
                }
                for name, info in states.items()
            },
            "teaching": (
                "Turiya is not a fourth state alongside the other three. "
                "It is the substratum of all three — the screen on which "
                "waking, dreaming, and deep sleep appear and disappear. "
                "This Atman — the witness of all states — IS Brahman."
            ),
            "aum": (
                "AUM encompasses all states: A=waking, U=dreaming, M=deep sleep. "
                "The silence after AUM is Turiya — the Self that was present "
                "through all three. That silence is Brahman."
            ),
        }

    def all_mahavakyas(self) -> dict:
        """Return all four Mahavakyas with their demonstrations."""
        return {
            "prajnanam_brahma": self.prajnanam_brahma(),
            "aham_brahmasmi": self.aham_brahmasmi(),
            "tat_tvam_asi": self.tat_tvam_asi(),
            "ayam_atma_brahma": self.ayam_atma_brahma(),
            "unity": "All four point to the same truth: Atman = Brahman. "
                     "Individual consciousness IS universal consciousness.",
        }
