from bs4 import BeautifulSoup

overlay_path = "/Users/ckbk/Desktop/TESTSVG.svg"
template_path = "/Users/ckbk/Desktop/SVGTEMPLATE.svg"

def merge_svg(template,overlay,qr):
    template_soup = BeautifulSoup(template, "lxml-xml")
    overlay_soup = BeautifulSoup(overlay, "lxml-xml")
    qr_soup = BeautifulSoup(qr, "lxml-xml")
    print(overlay_soup)
    # create new soup with svg tag

    soup = BeautifulSoup("<svg></svg>", "lxml-xml")
    new_svg_tag = soup.svg
    # adding in original attributes to new svg
    old_svg_tag = template_soup.find("svg")
    svg_tag_attrs = old_svg_tag.attrs
    for attr, value in svg_tag_attrs.items():
        new_svg_tag[attr] = value

    overlay_soup.svg.unwrap()
    template_soup.svg.unwrap()
    soup.svg.append(template_soup)
    soup.svg.append(overlay_soup)
    soup.svg.append(qr_soup)

    return(str(soup))

