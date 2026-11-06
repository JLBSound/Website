# JLB Studios website

Static site with no framework. `python3 build.py` writes the finished site to `site/`, which can be uploaded to any web host.

- **Wording:** `src/*.html`. The shared header and footer are in `src/_layout.html`, and the quote form is in `src/_form.html`.
- **Design tokens:** the top of `static/assets/site.css`, measured from the logo.
- **Posters:** save as `static/assets/posters/<slug>.jpg`. The slugs are listed in `build.py`.

## Before launch

- Add the poster images, after confirming permission to show them.
- Set `data-endpoint` in `src/_form.html` to a form service URL. Until then the form opens a pre-filled email.
- Add the reel and a producer quote where the HTML comments in `src/index.html` mark their place.
- Keep the page addresses when moving from Weebly so existing links still work.
