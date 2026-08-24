# Primes & Zooms — New Arrivals Notice Board

A3 notice board system for displaying new rental inventory arrivals at the Pune store.

## Deliverables for Printing

### File 1 — A3 Poster (Permanent Background)
**`Primes_&_Zooms_-_New_Arrivals_A3_Poster.pdf`**

The fixed background poster mounted on one side of the notice board. Printed once — staff write equipment names into the blank slots with a marker as new arrivals come in.

- 5 numbered slots (1–5), each `255mm × 54mm`
- Clean white/red P&Z branding
- Empty name lines for handwritten entries
- Print on A3, 100% scale, no fit-to-page

### File 2 — Ready-to-Cut Strips
**`Primes & Zooms — Notice Board Strips.pdf`**

Printable strips that match the poster slot dimensions exactly. Cut along dashed lines and pin onto the corresponding poster slots.

- 5 numbered slots (1–5), each `255mm × 54mm`
- Clean white/red P&Z branding
- Empty name lines for handwritten entries
- Print on A3, 100% scale, no fit-to-page

### File 2 — Ready-to-Cut Strips
**`Primes & Zooms — Notice Board Strips.pdf`**

Printable strips that match the poster slot dimensions exactly. Cut along dashed lines and pin onto the corresponding poster slots.

- 5 items: slots 1–5 (all slots in use)
- Each strip = `255mm × 54mm` (exact poster slot match)
- Each strip has: slot number badge, product name, short description, QR code linking to product page
- Print on A3, 100% scale, no fit-to-page

## Source Files

| File | Description |
|------|-------------|
| `items.json` | Single source of truth for product data |
| `poster.html` | A3 poster template (source of the poster PDF) |
| `generate-pdf.py` | Python script that generates the strips PDF with QR codes |
| `new-arrivals-qr-strips.html` | Browser-viewable version of the strips (fetches from items.json) |
| `archive/` | Previous A4 versions (kept for reference) |

## How to Update Strips

When new products arrive, edit `items.json`:
1. Add/update the `items` array with product info (slot, name, desc, url)
   - Ensure each item has a unique slot number (1-5) and that no items are repeated
   - **Sort items by rental price (5-day rate) in descending order**: most expensive items get Slot 1 (top position), followed by next highest in Slot 2, etc.
2. Run: `make strips` (or `python3 generate-pdf.py`)
3. The script outputs a timestamped PDF: `Primes & Zooms — Notice Board Strips_YYYYMMDD_HHMMSS.pdf`

Dependencies: `pip3 install qrcode weasyprint --break-system-packages`

## Dimensions

- Page: A3 portrait (`297mm × 420mm`)
- Each poster slot: `255mm × 54mm`
- Each strip: `255mm × 54mm` (cut from A3, 4 strips + cut-line gaps)

## Brand

- Primary: Red `#cb1513`, Dark `#222`
- Fonts: Barlow Semi Condensed (headings), Open Sans (body)
- URL: https://primesandzooms.com

## File Persistence

- **HTML files** (`new-arrivals-qr-strips.html`, `notice-board-publisher.html`, `poster.html`) remain in the project until explicitly deleted by the user
- **PDF outputs** are timestamped to preserve generation history: `Primes & Zooms — Notice Board Strips_YYYYMMDD_HHMMSS.pdf`
- Use `make clean` to remove all PDF files if needed (HTML files are preserved)
