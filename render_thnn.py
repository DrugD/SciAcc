import pymupdf, os
p = "/Users/likun/Desktop/paper-SciPro/Papers/Tensorized Hypergraph Neural Networks.pdf"
outd = "/Users/likun/Desktop/paper-SciPro/Outputs/images/THNN"
os.makedirs(outd, exist_ok=True)
doc = pymupdf.open(p)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    fn = os.path.join(outd, f"page{i+1:02d}.png")
    pix.save(fn)
    print(f"wrote {fn} ({pix.width}x{pix.height})")
doc.close()
