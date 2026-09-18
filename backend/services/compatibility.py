def check_compatibility(vessel, port):
    """
    Check whether a vessel is compatible with a port
    based on vessel dimensions and port limitations.
    """

    checks = {}

    # ---------------------------------------------
    # Length compatibility
    # ---------------------------------------------

    checks["length"] = (
        vessel["length"] <= port["max_length"]
    )

    # ---------------------------------------------
    # Draft compatibility
    # ---------------------------------------------

    checks["draft"] = (
        vessel["draft"] <= port["max_draft"]
    )

    # ---------------------------------------------
    # Overall compatibility
    # ---------------------------------------------

    compatible = all(checks.values())

    # ---------------------------------------------
    # Generate explanation
    # ---------------------------------------------

    reasons = []

    if not checks["length"]:
        reasons.append(
            f"Vessel length ({vessel['length']} m) "
            f"exceeds port maximum ({port['max_length']} m)."
        )

    if not checks["draft"]:
        reasons.append(
            f"Vessel draft ({vessel['draft']} m) "
            f"exceeds port maximum ({port['max_draft']} m)."
        )

    if compatible:
        reason = "Vessel is compatible with the port."
    else:
        reason = " ".join(reasons)

    return {
        "compatible": compatible,
        "checks": checks,
        "reason": reason
    }