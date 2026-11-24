"""Turns the example notebooks into pages of the documentation."""

c = get_config()  # type: ignore[name-defined]  # noqa: F821

c.TemplateExporter.template_file = "scripts/example.md.j2"
# Maps are pages of their own.
c.ExtractOutputPreprocessor.extract_output_types = {"image/png", "image/jpeg", "text/html"}
# Cells that install packages in Colab.
c.TagRemovePreprocessor.enabled = True
c.TagRemovePreprocessor.remove_cell_tags = {"colab"}
c.ExecutePreprocessor.skip_cells_with_tag = "colab"
