## What and why

<!-- The change, and the requirement or decision record it serves. -->

## Braids contribution checklist

Normative behaviour changes need these; a typo fix does not.

- [ ] Requirement or ADR this implements
- [ ] Positive conformance fixture
- [ ] Negative or edge fixture where misuse is plausible
- [ ] `docs/28` traceability updated

## Verification

<!-- What you ran, and what it proved. Say what you did NOT check. -->

```
python3 scripts/validate.py
python3 scripts/run_evals.py --fixture-tests
python3 scripts/measure_budget.py
python3 -m unittest discover -s tests
```

## Claims

<!-- If this PR claims faster, safer, more reliable or more compatible, name the evidence. Unverified is an acceptable answer; unstated is not. -->
