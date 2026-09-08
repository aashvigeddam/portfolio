# Working agreements for this site

## Always show a preview before anything ships

Every change to this site gets a **rendered preview of exactly how it will
look**, sent together with the change, before it is deployed. This holds for
any visual change and especially for design work. A description of the change
is not a preview; the rendered page is.

- Render the routes the change touches at desktop (1440x900) and phone
  (390x844), and send the images.
- When something moved or was restyled, show it **before and after**.
- Crop to the piece that changed on a large page; send the whole page when
  the change affects layout.
- Say plainly if a preview can't show something (hover, video playback,
  a live send) and describe that part instead.

## Rendering a preview

The site is one static `index.html` behind several routes, so it needs to be
served with the real headers to render correctly:

```
python3 tools/update-csp-hash.py          # after ANY index.html edit
python3 <scratchpad>/cspserve.py &        # replays vercel.json headers,
                                          # maps /about /work /contact
```

Then screenshot with Playwright (`playwright-core`, Chromium at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`). Wait for every image
to decode before capturing, or frames differ between runs for reasons that
have nothing to do with the change:

```js
await pg.waitForFunction(() => [...document.images]
  .filter(i => i.getAttribute('src'))
  .every(i => i.complete && i.naturalWidth > 0));
```

Headless Chromium here has no H.264, so video frames must come from ffmpeg
(`python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`).

## Delivery

Changes reach the live site as a zip she extracts and deploys herself
(`npx.cmd vercel --prod` on Windows). Always state the zip's byte size and the
byte size of `index.html` inside it, so a half-finished download is caught
before it is deployed — that has happened more than once.
