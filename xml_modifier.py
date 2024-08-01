from bs4 import BeautifulSoup
import re


def overlay_modifier(overlay_str):
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

    # get everytag, go throught their attributes and if it has class attributes, grab the values and modify it
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

# def get_qr_placeholder_attributes(overlay_path):
#     with open(overlay_path, "r") as f:
#         soup = BeautifulSoup(f, "lxml-xml")
#
#     return []

with open('./test.svg', "r") as file:
    qr = file.read()

# height="82.23" width="82.23" x="177.15" y="32.13"
def qr_modifier(qr_str, qr_attributes):
    qr_relative = qr_str.replace("mm",'')

    qr_soup = BeautifulSoup(qr_relative, "lxml-xml")

    og_height = qr_soup.svg["height"]
    height_ratio = float(qr_attributes["height"])/float(og_height)
    print(height_ratio)
    og_width = qr_soup.svg["width"]
    width_ratio = float(qr_attributes["width"])/float(og_width)
    print(width_ratio)

    qr_soup.svg['x'] = qr_attributes["x"]
    qr_soup.svg['y'] = qr_attributes["y"]
    qr_soup.svg['width'] = qr_attributes["width"]
    qr_soup.svg['height'] = qr_attributes["height"]

    for i in qr_soup.find_all("rect"):
        i["height"] = float(i["height"])*height_ratio
        i["width"] = float(i["width"])*width_ratio
        i["x"] = float(i["x"])*width_ratio
        i["y"] = float(i["y"])*height_ratio

    return(str(qr_soup))

if __name__ == "__main__":
    qr_attributes = {'width': '82.23', 'height': '82.23', 'x': '177.15', 'y': '32.13'}
    qr_modifier(qr,qr_attributes)

    overlay_path = "/Users/ckbk/Desktop/overlay.svg"
    with open(overlay_path, "r") as f:
        overlay_str = f.read()
    overlay_modifier(overlay_str)


