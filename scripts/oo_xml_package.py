import os
from lxml import etree

PACKAGE_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"


class OOXMLPackageBuilder:
    """
    Builds Office Open XML package metadata (OPC layer).
    Ensures DOCX compliance beyond minimal document.xml-only builds.
    """

    def build_content_types(self):
        root = etree.Element("Types", xmlns=CONTENT_TYPES_NS)

        etree.SubElement(
            root,
            "Default",
            Extension="rels",
            ContentType="application/vnd.openxmlformats-package.relationships+xml"
        )

        etree.SubElement(
            root,
            "Default",
            Extension="xml",
            ContentType="application/xml"
        )

        etree.SubElement(
            root,
            "Override",
            PartName="/word/document.xml",
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
        )

        etree.SubElement(
            root,
            "Override",
            PartName="/word/styles.xml",
            ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"
        )

        etree.SubElement(
            root,
            "Override",
            PartName="/docProps/core.xml",
            ContentType="application/vnd.openxmlformats-package.core-properties+xml"
        )

        return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

    def build_root_rels(self):
        root = etree.Element("Relationships", xmlns=PACKAGE_NS)

        etree.SubElement(
            root,
            "Relationship",
            Id="rId1",
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
            Target="word/document.xml"
        )

        return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
