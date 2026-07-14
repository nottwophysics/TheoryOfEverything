# `philosophy/` — the interpretive layer (NOT empirical)

> **This package is interpretive scaffolding, not physics.** Nothing in it is a
> measurement, a derivation from first principles, or a testable prediction. It
> is a computational *analogy* to Advaita Vedanta metaphysics. Do not read any
> output of these modules as an empirical claim about the physical world.

## Why this is walled off

The wider repository mixes three very different kinds of content:

1. **Computational-physics demos** (`gravity/`, `quantum/`, `particles/`) —
   real, checkable numerics that stand on their own terms.
2. **Numerology diagnostics** (`numerology/`) — explicitly labelled searches for
   coincidental formulas (see the look-elsewhere and cross-validation modules).
3. **This philosophy layer** — an Advaita-Vedanta interpretation expressed in
   code.

Keeping the philosophy in its own clearly-labelled package serves both
directions of honesty:

- It stops the interpretive modeling from being **mistaken for physics** — no
  reader should think `Brahman.compute(...)` measures anything about nature.
- It stops the physics modules from being **dismissed by association** — the
  emergent-gravity and tensor-network work should be judged as computational
  physics regardless of one's view of the metaphysics.

## What lives here

| Sub-package | Advaita concept | What the code models |
|---|---|---|
| `brahman/`     | Brahman, Sat-Chit-Ananda | non-dual consciousness as an undifferentiated ground; being/awareness/bliss decomposition |
| `maya/`        | Māyā, adhyāsa, nāma-rūpa, the three guṇas | superimposition of appearance on the ground; name-and-form individuation; sattva/rajas/tamas dynamics |
| `levels/`      | the three levels of reality | pāramārthika (absolute), vyāvahārika (empirical), prātibhāsika (illusory), and a "reality engine" relating them |
| `liberation/`  | neti-neti, the mahāvākyas | the "not this, not this" negation procedure; the great sayings (e.g. *tat tvam asi*) |

## Status of the claims

The framework's own `falsification/` module already concedes that the Advaita
interpretation is **not scientific** — it states plainly which parts of the
project can be falsified and which cannot, and this layer falls entirely on the
"cannot" side. That is not a defect to hide; it is the correct classification of
philosophy. This README simply makes the boundary explicit at the package level.

## Using it

The modules import and run as before — only their import path changed:

```python
# before:  from brahman.consciousness import Brahman
from philosophy.brahman.consciousness import Brahman
from philosophy.maya.gunas import Gunas, GunaBalance
from philosophy.levels.reality_engine import RealityEngine
from philosophy.liberation.neti_neti import NetiNeti
```
