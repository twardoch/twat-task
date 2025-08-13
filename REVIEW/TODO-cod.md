---
title: Improvement Plan and Proposals
this_file: REVIEW/TODO-cod.md
generated_by: codex-cli
generated_at: 2025-08-13
---

# twat-task – Improvement Plan (Detailed, Example-Illustrated)

This plan proposes focused, incremental improvements. It does not change code outside the REVIEW folder. Items are designed to be shippable in small PRs, with examples where relevant.

## Objectives

- Increase reliability of repo automation (cleanup, CI, versioning)
- Tighten developer experience (DX) via consistent tooling (Hatch/UV, pre-commit)
- Clarify docs and examples to reflect current capabilities
- Prepare for future real processing backends while preserving current mocks

## Phase 1 — Repo Hygiene and Tooling Consistency

- Cleanup script alignment
  - Remove hard dependency on `.cursor/rules/0project.mdc` (file not present); degrade gracefully instead of error logging in `REQUIRED_FILES` and `prefix()`.
  - Prefer checking presence with guidance instead of marking as required.
  - Replace ad-hoc venv management calls with Hatch scripts where possible (keep `uv` as an option).

  Example (concept):
  ```python
  # cleanup.py (concept only)
  REQUIRED_FILES = ["README.md", "TODO.md"]  # remove 0project.mdc
  def prefix() -> None:
      # If present, include; otherwise, skip silently
      stmt = Path(".cursor/rules/0project.mdc")
      if stmt.exists():
          log_section("PROJECT STATEMENT", stmt.read_text())
  ```

- Pre-commit versions
  - Harmonize versions in `.pre-commit-config.yaml` with `pyproject.toml` (already close). Ensure hooks run Ruff format before lint for fewer diffs.
  - Add `end-of-file-fixer`, `debug-statements`, `mixed-line-ending` already present; keep.

- CI checks parity
  - Ensure GitHub Actions `push.yml` mirrors Hatch scripts: `hatch run check-all` per matrix.
  - Keep Ruff action (fast), but add a MyPy step that uses project config (or run via Hatch).

- Versioning runtime fallback
  - `__init__.py` imports `twat_task.__version__`. During editable installs without hatch build hook, this file might not exist.
  - Provide safe runtime fallback in `__init__.py` if import fails (e.g., read from `VERSION.txt` or set to `0.0.0+local`).

  Example (concept):
  ```python
  try:
      from twat_task.__version__ import version as __version__
  except Exception:
      __version__ = (Path(__file__).with_name("__version__.py").read_text().strip()
      version_file = Path(__file__).with_name("__version__.py")
      __version__ = version_file.read_text().strip() if version_file.exists() else "0.0.0+local"
  ```

## Phase 2 — Documentation and Examples

- README precision
  - Clarify current state: extraction/transcription are mocked; show exact outputs (e.g., JSON content for audio mock) and safety of re-runs due to Prefect caching.
  - Add troubleshooting notes for common issues (Prefect installation, missing FFmpeg when real backend is added later).

- Examples structure
  - Replace `examples/testprefect_example.py` with package-centric examples:
    - `examples/basic_usage.py` — the VideoTranscript example from README ready to run.
    - `examples/flow_only.py` — calling `process_video_flow.fn()` directly for test-like runs.

  Example snippet (basic_usage.py):
  ```python
  from pathlib import Path
  from twat_task import VideoTranscript

  video = Path("example.mp4")
  video.write_text("dummy")
  vt = VideoTranscript(video_path=video)
  print("Audio path:", vt.audio_path)
  print("Transcript:", vt.text_transcript)
  ```

## Phase 3 — Tests and Quality Gates

- Tests
  - Add test ensuring `__version__` import does not break in editable installs.
  - Add an integration-style test that runs the flow with real temp files (still mock tasks) and asserts caching behavior across multiple property accesses.

- Type checking and lint
  - Keep strict MyPy settings; ensure tests pass without relaxing them.
  - Keep Ruff rules; address minor rule suppressions if they obscure intent.

## Phase 4 — Future Backends (Optional Extras)

- Design optional extras for real processing:
  - `ffmpeg` for audio extraction (invoke via subprocess; validate presence; fallback to mock if missing).
  - `whisper` or `vosk` for transcription; expose through a strategy interface.

  Example interface sketch:
  ```python
  class AudioExtractor(Protocol):
      def extract(self, video: Path, audio: Path) -> None: ...

  class Transcriber(Protocol):
      def transcribe(self, audio: Path) -> str: ...

  # Default (mock) implementations can live beside real ones guarded by extras
  ```

- Configuration
  - Accept env/config to select backend: `TWAT_TASK_EXTRACTOR=ffmpeg|mock`, `TWAT_TASK_TRANSCRIBER=whisper|mock`.
  - Clear error messages and graceful fallback to mock when extras are unavailable.

## Phase 5 — Developer Experience

- Hatch scripts
  - Ensure `check-all` runs: Ruff format, Ruff lint, MyPy, Pytest with coverage (already defined; verify alignment).

- Makefile (optional)
  - Provide thin wrappers to Hatch for common tasks if contributors prefer `make`.

## Risks and Edge Cases

- Missing `__version__` at runtime in editable installs causing import error — addressed by fallback.
- `cleanup.py` side effects (creating/deleting venv, installing deps) may be slow in CI — limit in CI, prefer Hatch-managed steps.
- Prefect version pin vs. features — keep `>=3.1.0` but verify minimal features used.

## Testing Strategy

- Unit tests: tasks and flow behavior (already present), extend with version import and editable install scenarios.
- Integration tests: ensure flow caching semantics are preserved across property accesses.
- CI matrix: keep 3.10–3.12, run hatch `check-all` + artifact coverage output.

## PR Breakdown (Suggested)

1) chore: soften cleanup.py required-files and prefix handling; doc note
2) chore(ci): align workflows with hatch `check-all`; add mypy step
3) docs: refine README; add runnable examples
4) test: add version fallback test and integration flow cache test
5) feat(core): safe __version__ fallback for editable installs

Each PR small, independently mergeable, with clear changelog entries.

## Pull Request Template (proposed)

```
Title: <scope>: <concise summary>

Summary
- What changed and why

Changes
- [ ] Code/tests
- [ ] Docs
- [ ] CI/tooling

Verification
- [ ] hatch run check-all

Notes
- Risks, migration, follow-ups
```

