## Mathematical Test Quality

A test is only valid if it verifies **mathematical correctness** on a concrete object.

**BAD TESTS (Trivial/Useless):**
- Checking if a return value `is not None`
- Checking `isinstance(result, int)`
- Checking `len(roots) > 0`
- Identity checks: `assert L.dual().dual() == L` without testing what `L.dual()` actually is
- Tautological tests: `expected = L.signature(); assert L.signature() == expected`

**GOOD TESTS (Nontrivial/Substantive):**
- Constructing a specific, known lattice (e.g., $E_8$, the Leech lattice, or the hyperbolic lattice $U \oplus \langle -2 \rangle$)
- Manually hardcoding the known correct mathematical invariant
- Example: `assert L.signature() == (1, 1)`
- Example: `assert L.discriminant() == -4`
- Example: `assert len(L.roots()) == 240` for $E_8$
- Example: `assert L.is_unimodular() is True`
