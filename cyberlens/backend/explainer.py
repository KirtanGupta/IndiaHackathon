def explain_module(module_result: dict) -> str:
    module = module_result["module"]
    score = module_result["score"]
    severity = module_result["severity"]
    signals = module_result["matched_signals"]

    if module_result.get("source") == "inactive":
        return module_result["summary"]

    model_note = ""
    if module_result.get("label"):
        confidence = round(float(module_result.get("confidence", 0.0)) * 100, 1)
        model_note = f" Model label: {module_result['label']} ({confidence}% confidence)."

    if signals:
        signal_text = ", ".join(signals)
        return f"{module.title()} scored {score}/100 ({severity}) due to signals: {signal_text}.{model_note}"

    return f"{module.title()} scored {score}/100 ({severity}) with limited suspicious indicators.{model_note}"


def explain_reasoning(module_result: dict) -> list[str]:
    if module_result.get("source") == "inactive":
        return [module_result["summary"]]

    label = module_result.get("label", "unknown")
    confidence = round(float(module_result.get("confidence", 0.0)) * 100, 1)
    score = module_result.get("score", 0)
    severity = module_result.get("severity", "low")
    matched_signals = module_result.get("matched_signals", [])
    breakdown = module_result.get(
        "score_breakdown",
        {"model_component": 0, "heuristic_component": 0, "raw_heuristic_score": 0},
    )

    reasons = [
        f"The model predicted '{label}' with {confidence}% confidence.",
        (
            f"The final risk score is {score}/100 and is marked as {severity}. "
            f"That score blends model confidence with suspicious phrase detection."
        ),
        (
            f"Model contribution added {breakdown.get('model_component', 0)}/100, while suspicious signals added "
            f"{breakdown.get('heuristic_component', 0)}/100."
        ),
    ]

    if matched_signals:
        highlighted = ", ".join(matched_signals[:5])
        reasons.append(f"The strongest indicators found in the email were: {highlighted}.")
    else:
        reasons.append("No strong suspicious keywords or patterns were detected in the email text.")

    if label == "phishing":
        reasons.append("The email was categorized as phishing because the language pattern looks closer to scam or credential-harvesting messages than normal business mail.")
    elif label == "benign":
        reasons.append("The email was categorized as benign because the wording looks closer to a normal operational or informational message than a phishing attempt.")

    return reasons


def explain_scan(scan_result: dict) -> dict:
    module_explanations = {
        module["module"]: explain_module(module)
        for module in scan_result["ordered_modules"]
    }
    module_reasoning = {
        module["module"]: explain_reasoning(module)
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
        "reasoning": module_reasoning,
    }
