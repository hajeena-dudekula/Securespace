EDIT_KEYWORDS = {
    "edit", "modify", "update", "revise",
    "fill", "complete", "correct", "maintain", "write"
}


def suggest_permission(category, purpose, existing_permission=None):
    purpose_text = (purpose or "").lower()
    words = set(purpose_text.replace("-", " ").split())

    needs_edit = bool(words & EDIT_KEYWORDS)

    if needs_edit:
        permission = "edit"
        reason = "The stated purpose indicates that editing may be required."
    else:
        permission = "read"
        reason = "Read-only access follows the principle of least privilege."

    if category in {"Finance", "Personal"}:
        if not needs_edit:
            reason += " This category may contain sensitive information."
        else:
            reason += " Review carefully because this category may contain sensitive information."

    if existing_permission == "edit" and permission == "read":
        reason += " Existing Edit access is present; review it before making changes."

    elif existing_permission == "read" and permission == "edit":
        reason += " Existing Read access may need an owner-approved upgrade."

    return {
        "permission": permission,
        "reason": reason,
        "requires_owner_approval": True
    }
