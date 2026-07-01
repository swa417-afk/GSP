import zipfile
import os
import tempfile


class DocxRuntime:
    """
    Full DOCX package assembler.
    Produces valid .docx ZIP containers from compiled WordprocessingML.
    No mutation, no patching—pure build phase.
    """

    def __init__(self, xml_bytes: bytes):
        self.xml_bytes = xml_bytes

    def _write_static_parts(self, base_dir: str):
        word_dir = os.path.join(base_dir, "word")
        rels_dir = os.path.join(base_dir, "_rels")
        os.makedirs(word_dir, exist_ok=True)
        os.makedirs(rels_dir, exist_ok=True)

        # document.xml
        with open(os.path.join(word_dir, "document.xml"), "wb") as f:
            f.write(self.xml_bytes)

        # relationships
        with open(os.path.join(rels_dir, ".rels"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>')

        # content types
        with open(os.path.join(base_dir, "[Content_Types].xml"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>'
                    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                    '<Default Extension="xml" ContentType="application/xml"/>'
                    '<Override PartName="/word/document.xml" '
                    'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                    '</Types>')

    def build(self, output_path: str):
        tmp_dir = tempfile.mkdtemp()

        self._write_static_parts(tmp_dir)

        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(tmp_dir):
                for file in sorted(files):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, tmp_dir)
                    z.write(full_path, arcname)

        return output_path
