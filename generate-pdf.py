#!/usr/bin/env python3
"""Generate printer-ready A3 notice board strips PDF with QR codes."""

import json
import qrcode
from io import BytesIO
import base64
from pathlib import Path
from weasyprint import HTML
from datetime import datetime

POSTER_SLOT_WIDTH_MM = 255
POSTER_SLOT_HEIGHT_MM = 54
A3_WIDTH_MM = 297
A3_HEIGHT_MM = 420

def load_items(config_path: str = "items.json") -> list[dict]:
    with open(config_path, 'r') as f:
        data = json.load(f)
    return data.get("items", [])

def validate_dimensions(items: list[dict]) -> None:
    for item in items:
        if item["slot"] < 1 or item["slot"] > 5:
            raise ValueError(f"Slot {item['slot']} out of range (1-5)")

def qr_b64(url: str) -> str:
    qr = qrcode.QRCode(box_size=8, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#222222", back_color="#ffffff")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def build_html(items: list[dict]) -> str:
    strips_html = ""
    for i, item in enumerate(items):
        qr_data = qr_b64(item["url"])
        strips_html += f"""
        <div class="strip">
            <div class="slot-num">{item['slot']:02d}</div>
            <div class="strip-body">
                <div class="strip-info">
                    <h3>{item['name']}</h3>
                    <div class="desc">{item['desc']}</div>
                </div>
                <div class="qrcode-wrap">
                    <img src="data:image/png;base64,{qr_data}" alt="QR" width="132" height="132">
                </div>
            </div>
        </div>"""
        if i < len(items) - 1:
            strips_html += """
        <div class="cut-line">
            <span class="dash"></span>
            <span class="label">cut</span>
            <span class="dash"></span>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @page {{ size: 297mm 420mm; margin: 0; }}
  @font-face {{
    font-family: 'Barlow Semi Condensed';
    src: url('https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@400;600;700&display=swap');
  }}
  @font-face {{
    font-family: 'Open Sans';
    src: url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1123px; height: 1587px;
    font-family: 'Open Sans', 'Helvetica', sans-serif;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 80px 0 60px;
  }}
  .page-title {{
    font-family: 'Barlow Semi Condensed', 'Helvetica', sans-serif;
    font-weight: 700; font-size: 22px;
    color: #cb1513; text-transform: uppercase;
    letter-spacing: 3px; margin-bottom: 4px;
  }}
  .page-sub {{
    font-size: 12px; color: #999;
    margin-bottom: 36px; letter-spacing: 1px;
  }}
  .strips-wrap {{ display: flex; flex-direction: column; align-items: center; }}
  .strip {{
    width: 963px; height: 204px; display: flex; align-items: stretch;
    background: #fff; border: 2px solid #e0e0e0;
    border-radius: 12px; overflow: hidden;
  }}
  .slot-num {{
    background: #cb1513; color: #fff;
    font-family: 'Barlow Semi Condensed', 'Helvetica', sans-serif;
    font-weight: 700; font-size: 36px;
    width: 85px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }}
  .strip-body {{
    flex: 1; padding: 20px 32px; display: flex; align-items: center; gap: 24px;
  }}
  .strip-info {{ flex: 1; min-width: 0; }}
  .strip-info h3 {{
    font-family: 'Barlow Semi Condensed', 'Helvetica', sans-serif;
    font-weight: 700; font-size: 28px; color: #222; line-height: 1.2; margin-bottom: 4px;
  }}
  .strip-info .desc {{ font-size: 14px; color: #666; line-height: 1.4; }}
  .qrcode-wrap {{
    width: 144px; height: 144px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    background: #fff; border: 1px solid #e0e0e0; border-radius: 8px;
    padding: 6px;
  }}
  .qrcode-wrap img {{ width: 132px; height: 132px; display: block; }}
  .cut-line {{
    height: 22px; display: flex; align-items: center; justify-content: center; gap: 6px;
  }}
  .cut-line .dash {{ display: block; width: 90px; height: 0; border-top: 1.5px dashed #bbb; }}
  .cut-line .label {{
    font-size: 9px; color: #bbb; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;
  }}
  .page-instructions {{ margin-top: auto; font-size: 10px; color: #bbb; text-align: center; letter-spacing: 1px; line-height: 1.6; }}
</style>
</head>
<body>
<div class="page-title">Primes &amp; Zooms — New Arrivals</div>
<div class="page-sub">Notice Board Strips · Cut &amp; Pin onto A3 Poster</div>
<div class="strips-wrap">{strips_html}</div>
<div class="page-instructions">
★ A3 · Print at 100% scale (no fit-to-page) · Cut along dashed lines · Each strip = 255mm × 54mm (matches poster slot)
</div>
</body>
</html>"""

if __name__ == "__main__":
    items = load_items()
    validate_dimensions(items)

    html_str = build_html(items)
    
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(__file__).parent / f"Primes & Zooms — Notice Board Strips_{timestamp}.pdf"

    html = HTML(string=html_str, base_url=str(Path(__file__).parent))
    html.write_pdf(str(out_path))
    print(f"PDF written to: {out_path}")