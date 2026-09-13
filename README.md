# CueG Lab — CueLee Quantitative Genetics Lab

Portable HTML and CSS with three pages: Home, Publications, and Contact. No JavaScript, build dependencies, external fonts, or host-specific services are needed to view the site.

## Edit and prepare for publishing

Edit the seven source files in the project root:
`index.html`, `publications.html`, `contact.html`, `style.css`, `favicon.svg`, `profile.jpg`, and `CV.pdf`.

Then run:

```sh
python3 scripts/build_site.py
```

This validates the source site, copies only the seven approved files into `publish/`, and validates the output. Existing generated files are refreshed. If the folder contains an unexpected file or a symlink, the script stops for review rather than copying or deleting it. Do not edit generated files in `publish/`; edit the root files and rebuild.

Preview the exact publishing output:

```sh
python3 -m http.server 8001 --bind 127.0.0.1 --directory publish
```

Open http://localhost:8001. Upload the **contents** of `publish/` to the destination web directory on Pitt hosting.

## Git and hosting are separate

`.gitignore` excludes generated `publish/`, local `private/`, Finder files, and Python caches from new Git tracking. It does not control deployment, hide already tracked files, remove Git history, or change the GitHub Pages source.

The build script's explicit file list is what controls the publishing package. GitHub Pages will not automatically use this ignored folder: a future GitHub Actions deployment must run the script and deploy `publish/`, or the current root-based deployment can continue to serve the source site. Do not assume root-based hosting excludes every non-website file.

No remote settings, commits, pushes, or deployments have been performed by the publishing script.

## Photograph

`profile.jpg` is a 1200 × 900 web JPEG, approximately 170 KB, preserving the full image. The original 4032 × 3024 photograph is retained at `private/profile-original.jpg` (approximately 3 MB). The backup is local and ignored by Git; keep it in your normal backup system.

For a replacement photo, retain the original in `private/`, export an appropriately sized JPEG as `profile.jpg`, and rebuild. Preserve the aspect ratio and review the result. No generated retouching is used.

## Maintenance

- Keep navigation and footer details synchronized across the three HTML files.
- Replace `CV.pdf` when your CV changes, then rebuild.
- Update publications in reverse year order, preserving year anchors and authorship markers.
- Lab name: CueG Lab (pronounced “cue-jee”); full name: CueLee Quantitative Genetics Lab. Keep the name consistent across all three titles and headers.
- Keep internal URLs relative so the site can move to a university subdirectory.
- Add People or Teaching only when confirmed content warrants another page.
- Run `python3 scripts/check_site.py` for source checks, or `python3 scripts/check_site.py publish` for the output.
- Review mobile layout and navigation after changes.
