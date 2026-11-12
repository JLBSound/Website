# JLB Studios website

Static site with no framework. `python3 build.py` writes the finished site to `site/`, which can be uploaded to any web host.

- **Wording:** `src/*.html`. The shared header and footer are in `src/_layout.html`, and the quote form is in `src/_form.html`.
- **Design tokens:** the top of `static/assets/site.css`, measured from the logo.
- **Posters:** save as `static/assets/posters/<slug>.jpg`. The slugs are listed in `build.py`.

## Publishing

Every push to `main` on GitHub (JLBSound/Website) builds the site and uploads changed files to Bluehost over FTPS (`.github/workflows/deploy.yml`). It needs three repository secrets: `FTP_SERVER`, `FTP_USERNAME` and `FTP_PASSWORD`.

- The reel video (`static/assets/reel/*.mp4`) is kept out of Git because of its size. Upload new reel files to `public_html/assets/reel` through cPanel File Manager.
- The old Weebly site is backed up on the server in `public_html/weebly-backup-2026-11-12`.
- `public_html/heroeslikeyou` belongs to heroeslikeyou.com. Leave it alone.
