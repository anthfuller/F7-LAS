package f7las.l5.enforcement

#
# F7-LAS Layer 5 — PDP (Policy Decision Point)
# Hard guardrails for destructive or high-impact actions.
#

default allow = false

#
# --- Rule: Allow safe READ-ONLY actions ---
#
allow {
    startswith(input.action, "get_")
}

allow {
    startswith(input.action, "list_")
}

allow {
    startswith(input.action, "describe_")
}


#
# --- Rule: Allow controlled destructive actions ---
# Allowed IFF:
#   - NOT production
#   - AND time_ok == true (outside change freeze)
#
allow {
    input.action == "terminate_instance"
    input.environment != "production"
    input.current_time_ok_for_change == true
}


#
# --- Deny reason (single rule, deterministic) ---
#
deny_message = msg {
    not allow

    # Case 1 — production modification denied
    input.action == "terminate_instance"
    input.environment == "production"
    msg := "Denied: terminate_instance blocked in production outside approved change window."
} else = msg {
    not allow
    msg := "Denied: action not allowed under current Layer-5 hard guardrails."
}
