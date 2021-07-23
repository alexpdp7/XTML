#!/usr/bin/env python3
import json
import subprocess
import sys
from xml.etree import ElementTree as ET


def to_xml_root(parsed):
    xtml =  ET.Element("xtml")
    for part in parsed[1:]:
        to_xml(part, parent=xtml)
    return xtml


def to_xml_paragraph(parsed, parent):
    paragraph = ET.SubElement(parent, "paragraph")
    for child in parsed["children"]:
        to_xml(child, parent=paragraph)
    return paragraph


def to_xml_line(parsed, parent):
    if not parent.text:
        parent.text = ""
    else:
        parent.text += " "
    parent.text += parsed["children"][0]


TYPE_TO_PARSER = {
    "paragraph": to_xml_paragraph,
    "line": to_xml_line,
}


def to_xml(parsed, **kwargs):
    if isinstance(parsed, list) and parsed[0] == "XTML":
        return to_xml_root(parsed)
    if isinstance(parsed, dict) and "type" in parsed:
        return TYPE_TO_PARSER[parsed["type"]](parsed, **kwargs)
    assert False, f"unparseable {parsed}"


def main(file):
    parser = subprocess.run(["instaparse-cli", "xtml.ebnf", file], stdout=subprocess.PIPE, encoding="utf8", check=True)
    parsed = json.loads(parser.stdout)
    xml = to_xml(parsed)
    ET.dump(xml)


if __name__ == "__main__":
    main(*sys.argv[1:])
