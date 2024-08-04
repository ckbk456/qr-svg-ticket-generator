import qrcode
import qrcode.image.svg
from bs4 import BeautifulSoup


def generate_qr(data):
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
        image_factory=factory,
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=0, )
    qr.add_data(data)
    qr.make(fit=True)

    qr_svg = qr.make_image(attrib={'class': 'some-css-class'})
    qr_svg_str = qr_svg.to_string(encoding="utf-8").decode("utf-8")

    return str(qr_svg_str)


def modify_qr(qr_str, qr_attributes):
    qr_relative = qr_str.replace("mm", '')
    qr_soup = BeautifulSoup(qr_relative, "lxml-xml")

    original_height = qr_soup.svg["height"]
    height_ratio = float(qr_attributes["height"]) / float(original_height)
    original_width = qr_soup.svg["width"]
    width_ratio = float(qr_attributes["width"]) / float(original_width)

    qr_soup.svg['x'] = qr_attributes["x"]
    qr_soup.svg['y'] = qr_attributes["y"]
    qr_soup.svg['width'] = qr_attributes["width"]
    qr_soup.svg['height'] = qr_attributes["height"]

    for i in qr_soup.find_all("rect"):
        i["height"] = float(i["height"]) * height_ratio
        i["width"] = float(i["width"]) * width_ratio
        i["x"] = float(i["x"]) * width_ratio
        i["y"] = float(i["y"]) * height_ratio

    return str(qr_soup)
