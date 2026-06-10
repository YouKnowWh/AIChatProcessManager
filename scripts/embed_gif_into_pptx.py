from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET


ROOT = Path("/Users/alex/Projects/AIChatProcessManager")
PPTX_PATH = ROOT / "AIChatProcessManager-complete-defense.pptx"
GIF_PATH = ROOT / "outputs" / "media" / "real-message-flow-terminal-real.gif"
TARGET_MEDIA = "/ppt/media/real-message-flow-terminal-real.gif"
SLIDE20_RELS = "ppt/slides/_rels/slide20.xml.rels"
CONTENT_TYPES = "[Content_Types].xml"

ns_ct = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
ns_rel = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}


def main():
    temp_path = PPTX_PATH.with_suffix(".tmp.pptx")

    with ZipFile(PPTX_PATH, "r") as zin, ZipFile(temp_path, "w", ZIP_DEFLATED) as zout:
        media_added = False
        for info in zin.infolist():
            data = zin.read(info.filename)

            if info.filename == CONTENT_TYPES:
                root = ET.fromstring(data)
                has_gif = any(
                    child.tag.endswith("Default") and child.attrib.get("Extension") == "gif"
                    for child in root
                )
                if not has_gif:
                    ET.register_namespace("", ns_ct["ct"])
                    root.insert(
                        2,
                        ET.Element(
                            "{http://schemas.openxmlformats.org/package/2006/content-types}Default",
                            {"Extension": "gif", "ContentType": "image/gif"},
                        ),
                    )
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True)

            elif info.filename == SLIDE20_RELS:
                root = ET.fromstring(data)
                for child in root:
                    if child.attrib.get("Type", "").endswith("/image"):
                        child.set("Target", TARGET_MEDIA)
                ET.register_namespace("", ns_rel["rel"])
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True)

            zout.writestr(info, data)

            if info.filename == "ppt/media/image3.png" and not media_added:
                zout.writestr(TARGET_MEDIA.lstrip("/"), GIF_PATH.read_bytes())
                media_added = True

        if not media_added:
            zout.writestr(TARGET_MEDIA.lstrip("/"), GIF_PATH.read_bytes())

    temp_path.replace(PPTX_PATH)
    print(PPTX_PATH)


if __name__ == "__main__":
    main()
