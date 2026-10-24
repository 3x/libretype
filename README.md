# Libretype (WIP)

> **Note:** this project is still in early development and is not ready for production use.

Libretype is a curated library of open-source fonts optimized for excellent web performance. The goal for this project is to be a suitable alternative to Google Fonts' CDN by focusing on:

- optimizing each font by hand,
- delivering the bare minimum number of characters to render your site in a user's preferred language,
- and comprehensive setup and troubleshooting instructions for both experienced and brand-new developers alike.

Libretype is being developed as a "version 2" of [xz/fonts](https://github.com/xz/fonts).

## Installation

WIP

## Building Fonts

`build.py` is an extremely bare-bones script for building a directory of TTF/OTF font source files into `.woff` and `.woff2` variants. This is a temporary tool I'm using as I experiment with optimizing file sizes and subsets, and will be replaced with a more stable build system in future updates.

## File Structure

Font source files, either in `.ttf` or `.otf` format, are sorted into the `font-sources/` directory.

### Static Fonts

Static fonts do not contain variable features and consist of separate files for each weight (thickness) and style (such as bold or italic). Families are stored in the `font-sources/static/` directory. File naming follows the syntax:

```
FONTNAME-WEIGHT-STYLE.(ttf|otf)
```

- `FONTNAME` is the font's slugified name (lowerspaced with whitespace characters replaced with a hyphen)
- `WEIGHT` is an integer corresponding to the face's weight. Font weights are typically given a name, like "Bold" for 700, but since these names are arbitrary and can differ between designers, the numeric weight is used instead. (For instance, "Bold" fonts are typically weighted 700, but the face _Go Bold_ actually has a weight of 600.) More information about font weight naming is available in the footnotes[^1]. Here are some common names given to different weight values:
  - `100`: "Thin"
  - `200`: "Extra Light" or "Ultra Light"
  - `300`: "Light"
  - `400`: "Regular" or "Normal"
  - `500`: "Medium"
  - `600`: "Semibold" or "Semi Bold"
  - `700`: "Bold"
  - `800`: "Extra Bold"
  - `900`: "Black" or "Heavy"
  - `950`: "Extra Black" or "Ultra Black" (sometimes `999`)
- `STYLE` is one of the following:
  - `normal`
  - `italic`
  - `oblique` (uncommon)

For example, here is the file layout for the font Go:

```
.
├── font-sources
│   ├── static
│   │   ├── go
│   │   │   ├── Go-Bold-Italic.ttf
│   │   │   ├── Go-Bold.ttf
│   │   │   ├── Go-Medium-Italic.ttf
│   │   │   ├── Go-Medium.ttf
│   │   │   ├── Go-Regular-Italic.ttf
│   │   │   └── Go-Regular.ttf

```

[^1]: Some helpful resources about font weight naming: [MDN's article on the CSS `font-weight` property](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-weight#meaning_of_relative_weights), [this gist from Łukasz Grolik](https://gist.github.com/lukaszgrolik/5849599), and [this Internet Archive snapshot of blog post from Bigelow & Holmes](https://web.archive.org/web/20150705025021/https://bigelowandholmes.typepad.com/bigelow-holmes/2015/07/on-font-weight.html), the designers of the _Lucida_ and _Windings_ font families.
