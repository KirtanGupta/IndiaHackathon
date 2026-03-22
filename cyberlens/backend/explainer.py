def explain_module(module_result: dict) -> str:
    module = module_result["module"]
    score = module_result["score"]
    severity = module_result["severity"]
    signals = module_result["matched_signals"]

    if module_result.get("source") == "inactive":
        return module_result["summary"]

    if signals:
        signal_text = ", ".join(signals)
        return f"{module.title()} scored {score}/100 ({severity}) due to signals: {signal_text}."

    return f"{module.title()} scored {score}/100 ({severity}) with limited suspicious indicators."


def explain_scan(scan_result: dict) -> dict:
    module_explanations = {
        module["module"]: explain_module(module)
        for module in scan_result["ordered_modules"]
    }

    active_phase = scan_result["active_phase"]
    active_result = scan_result["modules"][active_phase]
    overall = (
        f"{active_phase.title()} phase risk is {active_result['score']}/100 ({active_result['severity']}). "
        f"Only the {active_phase} model was used for this scan."
    )

    return {
        "overall": overall,
        "modules": module_explanations,
    }