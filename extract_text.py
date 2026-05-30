import os, sys, pymupdf

papers_dir = "/Users/likun/Desktop/paper-SciPro/Papers"
out_dir = "/Users/likun/Desktop/paper-SciPro/Outputs/text"
os.makedirs(out_dir, exist_ok=True)

for fn in sorted(os.listdir(papers_dir)):
    if not fn.lower().endswith(".pdf"):
        continue
    p = os.path.join(papers_dir, fn)
    doc = pymupdf.open(p)
    chunks = []
    for i, page in enumerate(doc):
        chunks.append(f"\n\n===== PAGE {i+1} =====\n" + page.get_text())
    doc.close()
    out = os.path.join(out_dir, fn.rsplit(".",1)[0] + ".txt")
    with open(out, "w") as f:
        f.write("".join(chunks))
    print(f"wrote {out} ({len(''.join(chunks))} chars)")
