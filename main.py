"""make.fun bounty: Sum up 25 November's world news in one image.

The entry program. It makes no network calls and uses no randomness: it
copies the finished image that ships in this repository (entry.png, a
1024x1024 PNG) to /output/entry.png. Running it twice writes the same bytes.
"""
import os


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    data = open(os.path.join(base, "entry.png"), "rb").read()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as handle:
        handle.write(data)
    print("Wrote /output/entry.png ({} bytes)".format(len(data)))


if __name__ == "__main__":
    main()
