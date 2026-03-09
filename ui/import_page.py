"""Statement import preview page skeleton."""

from nicegui import ui


def render_import_page() -> None:
    ui.label("Import Statement").classes("text-h4")
    ui.upload(label="Upload PDF/Image", auto_upload=False)
    ui.input("Optional PDF password", password=True, password_toggle_button=True)
    ui.button("Preview Import")
    ui.button("Confirm Import", color="primary")
    ui.markdown("Preview results will appear here.")
