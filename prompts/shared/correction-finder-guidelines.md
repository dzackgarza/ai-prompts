# Guidelines

Your task is to find OCR/correction errors where the extracted text is MATHEMATICALLY WRONG or UNREADABLE.

## Evidence Requirement

**Strong evidence is required.** Do not guess or rely on vague familiarity. Each declared error must be supported by clear, specific justification from the text itself.

## Acceptable Reasons to Report

- **Consistency contradiction**: The original contradicts itself or other visible content (e.g., "Let X be a variety. Then X is a scheme.")
- **Ill-defined notation**: The original would be mathematically undefined or nonsensical (e.g., "the group Z" without specifying Z of what)
- **Extremely well-known notation**: References to standard objects that are universally recognizable in the field (e.g., "Pic" -> "Pic" for Picard group, "Spec" for spectrum, "Hom" for hom-sets). Must be unambiguous.

## Not Allowed

- **Vague "well-known" appeals**: Claiming something is wrong without specific evidence from context
- **Equally valid interpretations**: Both the original and proposed correction are mathematically meaningful, and neither is contradicted by context
- **Unverifiable corrections**: No way to verify from the surrounding text whether the original or correction is correct

## REPORT (examples of valid errors)

- Wrong symbols: E for Σ (summation), E for ∈ (element-of), 0 for O (orthogonal group)
- Missing critical symbols that change meaning
- Subscripts/superscripts wrong so variables are unidentifiable
- Garbled words that make the sentence incomprehensible

## DO NOT REPORT

- Spacing issues: "$p$ -adic" vs "$p$-adic"
- Capitalization: "From" vs "from"
- Punctuation: missing periods, commas
- Hyphenation: "MordellWeil" vs "Mordell-Weil"
- LaTeX formatting: extra braces, spacing in math mode

## Output Format

Format each error as: `L###: "wrong" -> "right"`

Include a brief justification in your response if not obvious from context.
