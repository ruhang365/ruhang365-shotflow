# Launch demo

The launch asset is a real, ephemeral Codex CLI session using only the bundled
ShotFlow Skill, one accepted final frame, and one sentence. It submits no video
generation and records no reusable AI session.

Run either public-safe version:

```bash
bash launch/run-demo-en.sh
bash launch/run-demo-zh.sh
```

Recording checklist:

1. Show the attached final-frame filename and the one-sentence intent.
2. Show the complete Agent output and `Generation submitted: no`.
3. Keep the full terminal window inside a 16:9 capture; do not expose another
   app, account, notification, path outside the temporary demo directory, or
   provider credential.
4. Make a 9:16 crop/layout from the same recording; do not generate another
   video.
5. Keep the native recording outside Git and publish it only as a Release or
   social asset after approval.

The recording demonstrates the interface, not generated-video effectiveness.

The verified English capture is staged locally as
`dist/shotflow-v0.4.0-demo-en.mp4`. It is deliberately ignored by Git. Its
public-safe receipt and the exact Agent output are in `demo-assets.json` and
`demo-output-en.txt`.
