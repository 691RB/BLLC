import io, zipfile
from typing import List, Dict

def make_zip(files: List[Dict[str, str]]) -> bytes:
    """
    files: list of dicts with keys: name, content
    """
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            name = f.get("name") or f.get("filename") or "file.txt"
            content = f.get("content", "")
            zf.writestr(name, content)
    mem.seek(0)
    return mem.read()
