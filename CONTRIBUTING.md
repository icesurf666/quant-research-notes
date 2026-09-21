# Contributing

Public studies are append-only evidence packages. A pull request must explain:

1. which claim or implementation changed;
2. which source artifact supports the change;
3. whether published metrics changed;
4. why the manifest was regenerated.

Required before review:

```bash
make quality
```

Do not commit credentials, `.env` files, raw market data, private absolute paths,
or artifacts copied from the internal research repository without an explicit
public-release decision.

A green CI run is necessary, not sufficient. Result-changing pull requests must
also receive a manual evidence review before merge. On GitHub, protect `main`,
require the `quality` check, require one approving review, dismiss stale reviews,
and block force pushes and branch deletion.
