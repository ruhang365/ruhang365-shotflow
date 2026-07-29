# ShotFlow Pro boundary

ShotFlow Core is not a trial. It can plan, observe, diff, compile, and score a sequence entirely with local files and human observations.

## Proposed Pro beta

The first Pro capability is automatic video analysis:

- read a bound video and final frame;
- detect continuity facts with timestamped evidence;
- produce an `ObservationPatch` with confidence;
- let a human accept, edit, or reject the patch;
- keep the project portable back to Core.

Pro must use the public `ObservationPatch` and project schemas. It must not introduce a private-only project format, remove manual workflows, or make Core depend on membership.

## Activation gate

Do not create an empty private repository. Begin a working beta only after either:

- 200 public GitHub Stars; or
- five people complete a real Core project and request automated analysis.

Until then, Pro interest is collected through a labeled GitHub issue or discussion without asking users to publish private media.
