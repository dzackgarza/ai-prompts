# PDF Workflows

- PDF extraction: **LOAD `reading-pdfs` skill.** Use justfile recipes in `~/pdf-extraction`, not ad hoc installs.
  - Never: `pdftotext`, `pymupdf`, etc. Extremely low quality. Prefer e.g. `mineru`
