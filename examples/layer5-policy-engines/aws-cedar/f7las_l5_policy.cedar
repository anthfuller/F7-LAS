// F7-LAS L5 – Hard guardrail for terminate_instance

permit(
    principal,
    action == Action::"TerminateInstance",
    resource
)
when {
    context.environment != "production" &&
    context.current_time_ok_for_change == true
};

// Allow read-only actions in any environment
permit(
    principal,
    action in [
        Action::"DescribeInstance",
        Action::"ListInstances",
        Action::"GetInstanceHealth"
    ],
    resource
);
