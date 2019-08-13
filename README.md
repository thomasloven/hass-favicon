favicon
=======

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Change the favicon and app icons of your Home Assistant instance

![browser](https://user-images.githubusercontent.com/1299821/62975860-ad283a80-be1b-11e9-836a-d58a1732fb21.png)

# Installation instructions

- Copy the contents of `custom_components/favicon/` to `<your config dir>/custom_components/favicon/`.

- Get some icons

  There are some nice ones available [here](https://github.com/home-assistant/home-assistant-assets/tree/master/Alternates), and you can generate favicons from them using an online tool, such as [this one](https://realfavicongenerator.net/).

- Put your icons in e.g. `<your config dir>/www/favicons/`

- Add the following to your `configuration.yaml`:

```yaml
favicon:
  favicon: /local/favicons/favicon.ico
  apple: /local/favicons/apple-touch-icon-180x180.png
  32: /local/favicons/favicon-32x32.png
  512: /local/favicons/android-chrome-512x512.png
```

- Restart Home Assistant

- Make sure to clear the cache of your browser to get the new icons.

# Options

- `favicon` - an .ico file which is displayed in your browser tab or bookmark menu.

- `apple` - a 180 x 180 px image that will be displayed on your iDevice home screen if you save the link there

- `<number>` - a `<number>` x `<number>` px image that will be displayed wherever it's needed for non-apple devices.

You can add as few or as many of those you'd like. It's my understanding that the next smaller size will be used if one is requested which doesn't quite fit the need.

For reference, Home Assistant includes icons of sizes 192, 384, 512 and 1024 px square by default. Specifying even a single size will override all of those.

![it IS charging thankyouverymuch](https://user-images.githubusercontent.com/1299821/62975899-c29d6480-be1b-11e9-9b6b-9d160ef8b439.jpg)

---
<a href="https://www.buymeacoffee.com/uqD6KHCdJ" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
