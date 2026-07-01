import zipfile
import shutil
import os
import tempfile


def replace_section(docx_path, xml_block, marker_text):
    """
    Deterministically inject XML block into word/document.xml after marker_text.
    """

    tmp_dir = tempfile.mkdtemp()
    extract_path = os.path.join(tmp_dir, "docx")

    with zipfile.ZipFile(docx_path, 'r') as z:
        z.extractall(extract_path)

    doc_xml_path = os.path.join(extract_path, "word/document.xml")

    with open(doc_xml_path, "r", encoding="utf-8") as f:
        xml = f.read()

    if marker_text not in xml:
        raise ValueError("Marker text not found in document.xml")

    idx = xml.index(marker_text) + len(marker_text)
    new_xml = xml[:idx] + xml_block + xml[idx:]

    with open(doc_xml_path, "w", encoding="utf-8") as f:
        f.write(new_xml)

    new_docx = docx_path.replace(".docx", "_patched.docx")

    with zipfile.ZipFile(new_docx, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(extract_path):
            for file in sorted(files):
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, extract_path)
                z.write(full_path, arcname)

    return new_docx


if __name__ == "__main__":
    import sys

    docx_path = sys.argv[1]
    xml_block_path = sys.argv[2]
    marker = sys.argv[3]

    with open(xml_block_path, "r", encoding="utf-8") as f:
        xml_block = f.read()

    out = replace_section(docx_path, xml_block, marker)
    print(out)
