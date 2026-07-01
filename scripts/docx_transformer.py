import zipfile
import os
import tempfile
from lxml import etree

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _find_anchor(doc_tree, bookmark_name: str):
    """
    Locate a Word bookmarkStart element by name (structural anchor).
    No text/string matching is used.
    """
    xpath = f".//w:bookmarkStart[@w:name='{bookmark_name}']"
    results = doc_tree.xpath(xpath, namespaces={"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"})

    if not results:
        raise ValueError(f"Bookmark '{bookmark_name}' not found")

    return results[0]


def transform_docx(docx_path: str, xml_block: str, bookmark_name: str = "GSP_SECTION_8_2_ANCHOR"):
    """
    Fully structural DOCX transformation:
    - No string matching in document.xml
    - Uses WordprocessingML bookmark anchors
    - Deterministic unzip/rezip
    """

    tmp_dir = tempfile.mkdtemp()
    extract_path = os.path.join(tmp_dir, "docx")

    with zipfile.ZipFile(docx_path, "r") as z:
        z.extractall(extract_path)

    doc_xml_path = os.path.join(extract_path, "word/document.xml")

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(doc_xml_path, parser)
    root = tree.getroot()

    bookmark = _find_anchor(root, bookmark_name)

    parent_p = bookmark.getparent()
    grandparent = parent_p.getparent()

    insert_index = list(grandparent).index(parent_p) + 1

    fragment = etree.fromstring(f"<root>{xml_block}</root>")

    for i, node in enumerate(fragment):
        grandparent.insert(insert_index + i, node)

    tree.write(doc_xml_path, xml_declaration=True, encoding="UTF-8", standalone="yes")

    new_docx = docx_path.replace(".docx", "_patched.docx")

    with zipfile.ZipFile(new_docx, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root_dir, _, files in os.walk(extract_path):
            for file in sorted(files):
                full_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(full_path, extract_path)
                z.write(full_path, arcname)

    return new_docx


if __name__ == "__main__":
    import sys

    docx_path = sys.argv[1]
    xml_block_path = sys.argv[2]

    with open(xml_block_path, "r", encoding="utf-8") as f:
        xml_block = f.read()

    out = transform_docx(docx_path, xml_block)
    print(out)
