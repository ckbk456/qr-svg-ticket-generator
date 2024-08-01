import qrcode
import qrcode.image.svg
from bs4 import BeautifulSoup
# import qrcode.image.styles.
from xml_modifier import qr_modifier

# <rect class="cls-4" height="82.23" width="82.23" x="177.15" y="32.13"/>
def generate_qr(data):

    factory = qrcode.image.svg.SvgImage

    qr = qrcode.QRCode(
        image_factory=factory,
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=0,)
    qr.add_data(data)
    qr.make(fit=True)


    svg = qr.make_image(attrib={'class': 'some-css-class'})
    svg_bytes = svg.to_string(encoding="utf-8")
    svg_str = svg_bytes.decode("utf-8")
    return str(svg_str)

# def create_qr():
#     # qr_image = f"temp/{file_name}.png"
#     # overlay_pdf_name = f"temp/{file_name}overlay.pdf"
#     # ticket_pdf_name = f"final/{file_name}.pdf"
#
#     qr = QRCode(
#         version=1,
#         error_correction=constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=0,
#     )
#     qr.add_data(file_content)
#     qr.make(fit=True)
#
#     img = qr.make_image(fill_color="black", back_color="white")
#     print(type(img))  # qrcode.image.pil.PilImage
#     img.save(qr_image)