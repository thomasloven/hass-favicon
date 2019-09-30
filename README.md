favicon
=======

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Change the gui page title, favicon and app icons of your Home Assistant instance

![browser](https://user-images.githubusercontent.com/1299821/62975860-ad283a80-be1b-11e9-836a-d58a1732fb21.png)

# Installation instructions

- Copy the contents of `custom_components/favicon/` to `<your config dir>/custom_components/favicon/`.

- Get some icons

  There are some nice ones available [here](https://github.com/home-assistant/home-assistant-assets/tree/master/Alternates), and you can generate favicons from them using an online tool, such as [this one](https://realfavicongenerator.net/).

- Put your icons in e.g. `<your config dir>/www/favicons/`

## Method 1/2 Integration

- Go to your Home Assistant configuration and to Integrations

- Add a "Favicon" integration

- Enter what you want the title of the Home Assistant interface page to be, and the URL of the icons you wish to change. For the App icons there must be at least one specified. E.g. `favicon URL: /local/favicons/favicon.ico`, `iOS icon URL: /local/favicons/180x180.png`, `App icon 1024px URL: /local/favicons/1024x1024.png`.

- Press submit

- Refresh the page

![integration](https://user-images.githubusercontent.com/1299821/63462280-d91a7000-c45a-11e9-97af-52f0335cad66.gif)

## Method 2/2 YAML configuration

- Add the following to your `configuration.yaml` (For the icons-* there must be at least one of them specified):

```yaml
favicon:
  title: My Home
  favicon: /local/favicons/favicon.ico
  icon-apple: /local/favicons/apple-touch-icon-180x180.png
  icon-1024: /local/favicons/icon-1024x1024.png
  icon-512: /local/favicons/icon-512x512.png
  icon-384: /local/favicons/icon-384x384.png
  icon-192: /local/favicons/icon-192x192.png
```

- Restart Home Assistant

- Make sure to clear the cache of your browser to get the new icons.

### Options

- `title` - The title to display at the top of the window or browser tab.

- `favicon` - an .ico file which is displayed in your browser tab or bookmark menu.

- `icon-apple` - a 180 x 180 px image that will be displayed on your iDevice home screen if you save the link there

- `icon-*` - The app launcher icons for desktop and android phones. You need to specify at least one resolution (`1024, 512, 384, 192`) to make it work. Higher or lower resolutions will be created from the nearest size from your browser. The icons have to be png's.


![it IS charging thankyouverymuch](https://user-images.githubusercontent.com/1299821/62975899-c29d6480-be1b-11e9-9b6b-9d160ef8b439.jpg)

---
<a href="https://www.buymeacoffee.com/uqD6KHCdJ" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
