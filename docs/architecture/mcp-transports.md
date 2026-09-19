# Remote MCP transport options

## Disabling the standalone Streamable HTTP event stream

The controller and Go ADK normally open a standalone GET SSE stream after
initializing a Streamable HTTP MCP session. Some proxies buffer that stream's
headers, and some request/response-only MCP servers do not support it.

For servers that do not need server-initiated notifications, opt out per server:

```yaml
apiVersion: kagent.dev/v1alpha3
kind: RemoteMCPServer
metadata:
  name: request-response-tools
spec:
  description: Tools that only need request/response communication
  url: https://tools.example.com/mcp
  protocol: STREAMABLE_HTTP
  disableStandaloneSSE: true
```

This setting is honored by controller-side discovery and MCP Apps calls, and by
Go ADK tool discovery and execution. It is serialized into the Go ADK connection
parameters as `disable_standalone_sse`. Unset or `false` keeps the SDK default.

Only the **standalone** GET stream is disabled. POST initialization, tool listing,
tool calls, and streamed POST responses continue to work. Server-initiated
notifications delivered through the standalone stream, such as tool-list changes,
are no longer received. Leave the setting unset when those notifications are
required. The legacy `SSE` transport is unchanged and ignores this setting.

The Python runtime and native Claude/Codex clients do not implement this option.
The Claude and Codex harness compilers report a compatibility warning when it is
enabled, rather than claiming to enforce it. Use the Go ADK when this transport
behavior is required for agent execution.
