# Contributing

Thanks for helping improve LLM Proxy Doctor.

## Before opening a pull request

1. Keep the project dependency-free at runtime.
2. Add or update unit tests for behavior changes.
3. Keep API keys and endpoint credentials out of source code, test fixtures, and logs.
4. Preserve the documented exit-code contract.
5. Update the README or troubleshooting guide when CLI behavior changes.

## Run checks locally

```bash
python -m unittest discover -s tests -v
python -m compileall -q doctor.py tests
python doctor.py --help
```

If you use Ruff locally, run `ruff check .` and resolve newly introduced findings.

## Pull request checklist

- [ ] Tests cover the change.
- [ ] No secrets or personal endpoint data are included.
- [ ] Error messages are actionable and do not hide the underlying failure.
- [ ] Documentation and examples are accurate.
