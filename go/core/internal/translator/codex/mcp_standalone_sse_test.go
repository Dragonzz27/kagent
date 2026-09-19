package codex

import (
	"testing"

	"github.com/kagent-dev/kagent/go/api/v1alpha3"
	"github.com/stretchr/testify/require"
)

func TestStandaloneSSECompatibilityWarning(t *testing.T) {
	for _, disabled := range []*bool{nil, new(false), new(true)} {
		server := &v1alpha3.RemoteMCPServer{Spec: v1alpha3.RemoteMCPServerSpec{
			URL: "https://mcp.example.test", DisableStandaloneSSE: disabled,
		}}
		warning := codexMCPCompatibilityWarning(server)
		if disabled != nil && *disabled {
			require.Contains(t, warning, "disableStandaloneSSE")
		} else {
			require.Empty(t, warning)
		}
	}
}
