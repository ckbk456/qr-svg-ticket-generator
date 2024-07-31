from bs4 import BeautifulSoup
import re


def overlay_modifier(overlay_soup):
    soup=overlay_soup
    def replace_class(match):
        replacement = "overlay-svg-" + match.group()
        return f"{replacement}"

    class_name_pattern = re.compile(r"(cls-[0-9]{0,})")
    style_text = soup.style.getText()
    modified_style_text = class_name_pattern.sub(replace_class, style_text)

    new_style = soup.new_tag("style")
    new_style.string = modified_style_text

    soup.style.decompose()
    soup.defs.append(new_style)

    # get everytag, go throught their attributes and if it has class attributes, grab the values and modify it
    all_elem = soup.find_all()
    for elem in all_elem:
        attributes_dict = elem.attrs
        for attribute, attribute_value in attributes_dict.items():
            if attribute == "class":
                new_attribute_value = class_name_pattern.sub(replace_class, attribute_value)
                elem[attribute]= new_attribute_value

    return(soup)


class QrAttributes:
    def __init__(self, overlay_path):
        with open(overlay_path, "r") as f:
            soup = BeautifulSoup(f, "lxml-xml")
        rectangle = soup.rect
        placeholder_rectangle_attribute = rectangle.attrs
        self.qr_x = placeholder_rectangle_attribute["x"]
        self.qr_y = placeholder_rectangle_attribute["y"]
        self.qr_width = placeholder_rectangle_attribute["width"]
        self.qr_height = placeholder_rectangle_attribute["height"]

# def get_qr_placeholder_attributes(overlay_path):
#     with open(overlay_path, "r") as f:
#         soup = BeautifulSoup(f, "lxml-xml")
#
#     return []

