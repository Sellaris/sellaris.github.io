# Hanrui Chen · 陈瀚锐

Bilingual academic homepage: https://sellaris.github.io/

Adapted from [Minimal Light](https://github.com/yaoyao-liu/minimal-light). Original theme license: CC0; see `LICENSE.minimal-light`.

## Editing

- `content.json`: profile, publications, news, and awards.
- `content.zh.json`: Chinese translations.
- `dist/assets/site.css`: shared styles. Award window heights are `220px` (international/national) and `180px` (regional/provincial/university).
- `dist/assets/`: images, CV, and supporting files.
- Run `python build.py` to generate both language pages.
- Preview with `python -m http.server 4174 --directory dist`.

Push to `main` to build and publish automatically through GitHub Actions and GitHub Pages.

## Visitor map

The left sidebar embeds a shared Flag Counter map in both languages. `content.json` contains its public image and statistics URLs under `visitor_map`. The external image records visits and shows approximate country locations and pageviews; click it for details. Statistics begin when the counter is created and do not include earlier traffic. No account was registered. To disable it, remove `visitor_map` and rebuild.
