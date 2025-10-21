import sys
import base64
import mimetypes
from pathlib import Path

from main import chain


def file_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/octet-stream"
    b = path.read_bytes()
    b64 = base64.b64encode(b).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "input.jpg"
    if arg.startswith("http://") or arg.startswith("https://") or arg.startswith("data:"):
        image_ref = arg
    else:
        p = Path(arg)
        if not p.exists():
            print(f"File not found: {p}")
            sys.exit(1)
        image_ref = file_to_data_uri(p)

    print("Invoking chain...\n")
    res = chain.invoke(image_ref)
    print("\n=== Result ===\n")
    print(res)


if __name__ == "__main__":
    main()
