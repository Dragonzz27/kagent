# KAgent Skills

Core library for discovering, parsing, and loading KAgent skills from the filesystem.

For example usage, see `kagent-adk` and `kagent-openai` packages.

## Shell command timeout

Set `KAGENT_COMMAND_TIMEOUT` to a positive whole number of seconds to override the
built-in `bash` tool's timeout, including Python commands. Both the Python skills
library and the Go ADK command executor honor this setting. For example, add the
following to a kagent `Harness`:

```yaml
spec:
  env:
    - name: KAGENT_COMMAND_TIMEOUT
      value: "120"
```

When unset, empty, invalid, or outside Go's `time.Duration` range, the existing
30-second default (60 seconds for Python commands) remains in effect. The setting
does not extend an earlier caller deadline or change the tool's arguments.
