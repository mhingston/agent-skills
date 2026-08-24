# Before-fix review record

- Condition: candidate, target `decision-continuity` loaded.
- Prompt: “Add a third router dimension” with the recorded re-entry evidence.
- Finding: the model located the evaluation fixture and proposed patching
  `references/examples.md` and `references/evaluation-suite.md` instead of
  returning a continuity report with a proposed supersession.
- Limitation: the read-only sandbox prevented the attempted write.
- Resolution: add the narrow fixture-as-read-only boundary to the active skill;
  the current paired record is in `candidate/run.md`.
