from services.permission_advisor import suggest_permission


def test_default_permission_is_read():
    result = suggest_permission("General", "")

    assert result["permission"] == "read"
    assert result["requires_owner_approval"] is True


def test_explicit_edit_purpose_suggests_edit():
    result = suggest_permission(
        "Work",
        "Please edit this document"
    )

    assert result["permission"] == "edit"


def test_finance_document_defaults_to_read():
    result = suggest_permission("Finance", "View the report")

    assert result["permission"] == "read"
    assert "sensitive" in result["reason"]


def test_existing_edit_permission_triggers_review_warning():
    result = suggest_permission(
        "General",
        "View the document",
        existing_permission="edit"
    )

    assert result["permission"] == "read"
    assert "Existing Edit access" in result["reason"]
