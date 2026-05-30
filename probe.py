import pymupdf
p = "/Users/likun/Desktop/paper-SciPro/Papers/Tensorized Hypergraph Neural Networks.pdf"
doc = pymupdf.open(p)
page = doc[0]
# Try different extraction modes
for mode in ["text", "blocks", "dict", "rawdict"]:
    try:
        r = page.get_text(mode)
        if mode in ("text",):
            print(f"=== {mode} ({len(r)} chars) ===")
            print(r[:500])
        else:
            print(f"=== {mode} (type={type(r).__name__}) ===")
            if isinstance(r, list):
                print(f"  {len(r)} items, first: {str(r[0])[:300] if r else 'none'}")
            elif isinstance(r, dict):
                print(f"  keys: {list(r.keys())[:5]}, blocks: {len(r.get('blocks',[]))}")
    except Exception as e:
        print(f"{mode}: error {e}")

# Check for images
imgs = page.get_images()
print(f"\nImages on page 1: {len(imgs)}")
# Check fonts / has text
print(f"Has text: {bool(page.get_text().strip())}")
# Check all objects
print(f"Page dict: {page.bound()}, rotation {page.rotation}")
