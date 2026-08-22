# BUILD.md — aashvigeddam.com v2 landing page

Handoff for Claude Code. The heavy lifting is done: assets are processed, the page is built, seven of thirteen slots are filled. Your job is to serve it, verify it, slot the remaining assets as Aashvi supplies them, and deploy to a preview URL.

## Project state

```
aashvi-landing/
  index.html        the complete landing page (works by opening it or via any static server)
  BUILD.md          this file
  assets/
    sf-background.mp4   Golden Gate + SF skyline, 10s loop, 1920x1080, 3.25MB, h264, no audio
    sf-poster.jpg       first frame, used while video loads and under reduced motion
    notebook.png        burgundy leather journal, monogram A     -> left of photo
    doodle-sun.png      gold sun charm                           -> upper-left of photo
    doodle-airplane.png paper airplane, lined paper              -> left of photo
    doodle-bouquet.png  peony bouquet sticker                    -> lower-left of photo
    doodle-disco.png    disco ball sticker                       -> upper-right of photo
    doodle-vinyl.png    vinyl record, "Limited edition"          -> lower-right of photo
    soc-mail.png        envelope-with-heart sticker              -> social row, links to mailto
```

All PNGs are background-removed (edge flood fill, threshold 247), trimmed, padded 10px, sized 189-435px on the long edge. Sticker die-cut borders on bouquet/disco/envelope are intact. Video was recompressed from 12.9MB (CRF 28, preset slow, faststart, audio stripped).

## How the page works

One fixed 1440x900 design canvas, cover-scaled to the viewport (`scale = max(vw/1440, vh/900)`), so the composition never reflows; it behaves like a poster that zooms. Every element's position is a row in the `LAYOUT` object: x, y, w, h in canvas pixels, r in degrees, optional href. Every asset path is a row in `ASSETS`; a null shows a labeled dashed placeholder instead. The background video is muted, looping, playsinline, with a poster fallback and a reduced-motion gate. The washed-out look is a CSS filter on the video (`saturate(.7) brightness(1.15)`) plus an 18% white scrim; tune those two values, never the video file.

## Remaining slots (null in ASSETS) and their specs

1. `photo` — Aashvi's photo, photobooth energy. Target box 320x465. Process: convert HEIC to PNG, desaturate to b&w, slight contrast lift. Keep rectangular with its border, no cutout.
2. `scrap-hi` + `scrap-welcome` — photographs of real handwritten torn paper. Cut out with transparent background same as the others (flood fill from edges, threshold 247, trim, 10px pad).
3. `deviceFrame` + `deviceVideo` — device PNG (camera/laptop) with its screen region transparent, plus the mp4 that plays inside on hover. After adding, set `deviceScreen` fractions to the actual screen rectangle within the PNG: x,y = screen's top-left as a fraction of image width/height, w,h likewise. Compress the video the same way as the background: `ffmpeg -i in.mov -an -c:v libx264 -crf 28 -preset slow -movflags +faststart out.mp4`.
4. `certstack` — fan of 2-3 certificate scans, top one near-straight. Compose in an editor or ask Claude Code to composite with PIL (rotate -6/0/+5 degrees, stack with drop shadows), export one PNG.
5. `soc-li`, `soc-gh` — two more sticker-style icons matching soc-mail's visual language. Wire hrefs in LAYOUT (LinkedIn URL is already set; GitHub pending).

## First session checklist

1. `python3 -m http.server 8000` in the project root, open localhost:8000, confirm: video plays and loops, seven real assets render in position, six placeholders show labels, no console errors.
2. Do not refactor index.html into a framework. It is a single static file on purpose.
3. When Aashvi supplies a pending asset: process per its spec above, drop in assets/, fill its ASSETS path, adjust its LAYOUT h to match the real aspect ratio (h = w / aspect), reload, screenshot, show her.
4. Nudge positions only at her direction; the current numbers are measured from the reference site.

## Deploy

New git repo in this folder (`git init`), never inside the existing aashvigeddam.com repo. Push to GitHub, import to Vercel as a static site, no build step. Preview URL only; do not attach the aashvigeddam.com domain. The live site stays untouched until she picks the winner.

## Acceptance before showing her

- Page loads under 5MB total transferred.
- Video loops without a visible stutter at the loop point (if the cut jumps, crossfade the loop: re-encode with the last 0.5s blended, or accept and note it).
- Every placed element sits inside the visible area at 16:9, 16:10, and an ultrawide test.
- Mobile: canvas cover-scales, socials remain tappable (44px targets after scale), video autoplays muted on iOS (playsinline present).
- Reduced motion shows the poster frame, not the video.
- Footer credit renders: "designed & developed by aashvi geddam · layout inspired by sebin jeon" (she may delete the second clause; her call).

## Reference image

`reference/sebinjeon-target.png` is a full-page screenshot of sebinjeon.com, the layout target. Use it two ways: as the visual comparison when tuning LAYOUT positions (open it side by side with localhost and match placement, scale, and spacing), and as the answer key for the pending slots (the compact camera top-right is the device slot's composition target; the poster fan below it is the certstack target; the photobooth photo center is the photo treatment target). Two hard rules: this file never leaves the reference/ folder and never deploys — add `reference/` to .gitignore before the first commit — and nothing inside it is ever cropped out for use as a page asset. It is Sebin Jeon's work and exists here only as a measuring stick.
