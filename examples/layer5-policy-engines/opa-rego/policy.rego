package agent.security.enforcement

default allow = false

# Allow read-only patterns
allow {
    startswith(input.action, "get_")
}
allow {
    startswith(input.action, "list_")
}
allow {
    startswith(input.action, "describe_")
}

# Conditional allow for terminate_instance
allow {
    input.action == "terminate_instance"
    input.environment != "production"
    input.current_time_ok_for_change == true
}

# Deny message
deny_message[msg] {
    not allow

    input.environment == "production"
    input.action == "terminate_instance"
    msg := "Agent action denied by L5 Policy: Production modification outside approved maintenance window."
}

deny_message[msg] {
    not allow

    not (input.environment == "production" && input.action == "terminate_instance")
    msg := "Agent action denied by L5 Policy: Action is not on the allowed list."
}
