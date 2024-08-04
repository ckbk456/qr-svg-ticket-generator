from bs4 import BeautifulSoup
import re


def modify_overlay_xml(overlay_str):
    soup = BeautifulSoup(overlay_str, "lxml-xml")
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
    print(soup.prettify())

    # get everytag, go through their attributes and if it has class attributes, grab the values and modify it
    all_elem = soup.find_all()
    for elem in all_elem:
        attributes_dict = elem.attrs
        for attribute, attribute_value in attributes_dict.items():
            if attribute == "class":
                new_attribute_value = class_name_pattern.sub(replace_class, attribute_value)
                elem[attribute]= new_attribute_value
        if elem.name == "text":
            for child in elem.findChildren():
                child.unwrap()
            text = elem.getText()
            tspan = BeautifulSoup().new_tag("tspan")
            tspan.string = text
            tspan['x'] = 0
            tspan['y'] = 0
            elem.string = ""
            elem.append(tspan)

    return str(soup)


def get_qr_attributes(overlay_str):
    soup = BeautifulSoup(overlay_str, 'lxml-xml')
    rectangle = soup.rect
    placeholder_rectangle_attribute = rectangle.attrs
    qr_x = placeholder_rectangle_attribute["x"]
    qr_y = placeholder_rectangle_attribute["y"]
    qr_width = placeholder_rectangle_attribute["width"]
    qr_height = placeholder_rectangle_attribute["height"]
    return {"width": qr_width, "height": qr_height, "x": qr_x, "y": qr_y}


def merge_xml(template, overlay, qr):
    template_soup = BeautifulSoup(template, "lxml-xml")
    overlay_soup = BeautifulSoup(overlay, "lxml-xml")
    qr_soup = BeautifulSoup(qr, "lxml-xml")
    # print(overlay_soup)
    # create new soup with svg tag

    soup = BeautifulSoup("<svg></svg>", "lxml-xml")
    new_svg_tag = soup.svg
    # adding in original attributes to new svg
    old_svg_tag = template_soup.find("svg")
    svg_tag_attrs = old_svg_tag.attrs
    for attr, value in svg_tag_attrs.items():
        new_svg_tag[attr] = value

    overlay_soup.svg.unwrap()
    overlay_soup.rect.decompose()
    template_soup.svg.unwrap()
    soup.svg.append(template_soup)
    soup.svg.append(overlay_soup)
    soup.svg.append(qr_soup)

    return str(soup)



