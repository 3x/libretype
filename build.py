"""
Script for building subsetted WOFF and WOFF2 files from a static font family.

Usage:
$ python build.py [font display name] [font slug]
"""

import sys
from pathlib import Path
from shutil import rmtree

from fontTools import subset

FONT_SOURCE_DIR = "font-sources/static"
OUTPUT_DIR = "output/s"
UNICODE_RANGES_DIR = "unicode-ranges"


def build_subset_args(family, file, woff_type, subset="everything"):
    output_file = f"{OUTPUT_DIR}/src/{family}/{file.stem}.{subset}.{woff_type}"

    unicodes_arg = "--unicodes=*"
    if subset != "everything":
        unicodes_arg = f"--unicodes-file={UNICODE_RANGES_DIR}/{subset}.txt"

    return [
        str(file),
        f"--output-file={output_file}",
        f"--flavor={woff_type}",
        unicodes_arg,
        "--with-zopfli",
        "--layout-features=*",
        "--hinting",
        "--desubroutinize",
    ]


def main():
    if len(sys.argv) == 3:
        font_name = sys.argv[1]  # Pretty name like "Go Mono"
        font_slug = sys.argv[2]  # Slug like "go-mono"
        print(f'Building font "{font_name}" with slug "{font_slug}".')

        # create output dir for built files
        Path(f"{OUTPUT_DIR}/src/{font_slug}").mkdir(exist_ok=True, parents=True)

        # identify the font source files to be processed
        files = list(Path(".").glob(f"{FONT_SOURCE_DIR}/{font_slug}/*.ttf"))

        # create a string to hold the generated CSS as it's built
        css = ""

        count = 1

        for file in files:
            file_name = file.stem

            print(f"Processing {file_name} ({count}/{len(files)})")
            count += 1

            style = file_name.split("-")[-1]
            weight = file_name.split("-")[-2]

            # step 1: everything

            subset.main(build_subset_args(font_slug, file, "woff"))
            subset.main(build_subset_args(font_slug, file, "woff2"))

            css += f"""/* everything */
@font-face {{
  font-family: "{font_name}";
  font-style: {style};
  font-weight: {weight};
  font-display: swap;
  src:
    url("src/{font_slug}/{file_name}.everything.woff2") format("woff2"),
    url("src/{font_slug}/{file_name}.everything.woff") format("woff");
}}
"""

            # step 2: just latin-ext

            subset.main(build_subset_args(font_slug, file, "woff", "latin-ext"))
            subset.main(build_subset_args(font_slug, file, "woff2", "latin-ext"))

            css += f"""
/* latin-ext */
@font-face {{
  font-family: "{font_name}";
  font-style: {style};
  font-weight: {weight};
  font-display: swap;
  src:
    url("src/{font_slug}/{file_name}.latin-ext.woff2") format("woff2"),
    url("src/{font_slug}/{file_name}.latin-ext.woff") format("woff");
  unicode-range: U+0100-036F, U+1D00-1DBF, U+1E00-1EFF, U+2020, U+20A0-20CF, U+2113, U+2C60-2C7F;
}}
"""
            # step 3: just latin-basic

            subset.main(build_subset_args(font_slug, file, "woff", "latin-basic"))
            subset.main(build_subset_args(font_slug, file, "woff2", "latin-basic"))

            css += f"""
/* latin-basic */
@font-face {{
  font-family: "{font_name}";
  font-style: {style};
  font-weight: {weight};
  font-display: swap;
  src:
    url("src/{font_slug}/{file_name}.latin-basic.woff2") format("woff2"),
    url("src/{font_slug}/{file_name}.latin-basic.woff") format("woff");
  unicode-range: U+0000-00FF, U+2000-206F, U+2190-2199, U+0131, U+0152, U+0153, U+02BB, U+02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+20AC, U+2122, U+2215, U+FEFF, U+FFFD;
}}
"""

        with open(f"{OUTPUT_DIR}/{font_slug}.css", "w") as css_file:
            css_file.write(css)

    else:
        print("error: exactly 2 arguments required")
        sys.exit(1)


if __name__ == "__main__":
    main()
