favicon
=======

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Change the gui page title, favicon and app icons of your Home Assistant instance

![browser](https://user-images.githubusercontent.com/1299821/62975860-ad283a80-be1b-11e9-836a-d58a1732fb21.png)

# Installation instructions

- Copy the contents of `custom_components/favicon/` to `<your config dir>/custom_components/favicon/`.

- Get some icons

  There are some nice ones available [here](https://github.com/home-assistant/iOS/tree/master/icons/Alternates), and you can generate favicons from them using an online tool, such as [this one](https://realfavicongenerator.net/).

- Put your icons in e.g. `<your config dir>/www/favicons/`. Note that `<your config dir>/www/` translates to `/local/` for the Icon path.
Note: If you created `<your config dir>/www/` you need to restart Home Assistant once before any icons will be found.

### About the icons
`hass-favicon` will scan the specified directory and automatically apply icons when found based on their filename. There are three types of icons, and it's important that you get the filenames correct.

- `favicon.ico` - The icon which is displayed on the browser tab and in the bookmark menu
- `favicon-apple-<anything>.png` - The icon which is displayed if you save your interface to the home screen of your iDevice.
- `favicon-<size>x<size>.png` - Used by android devices. `<size>` indicates the icon size in pixels, e.g. `favicon-1024x1024.png`.

## Method 1/2 Integration

- Go to your Home Assistant configuration and to Integrations

- Add a "Favicon" integration

- Enter your wanted title, the path to your icons (e.g. `/local/favicons/`), and launch icon color (e.g. `#BADA55`)

- Press submit

- Refresh the page. Make sure to clear the cache of your browser to get the new icons.

![integration](https://user-images.githubusercontent.com/1299821/65991117-1d068900-e48d-11e9-9002-f2253fafa190.gif)

## Method 2/2 YAML configuration

- Add the following to your `configuration.yaml`:

```yaml
favicon:
  title: My Home
  icon_path: /local/favicons/
  launch_icon_color: "#BADA55"
```

- Restart Home Assistant

- Make sure to clear the cache of your browser to get the new icons.

### Options

- `title` - The title to display at the top of the window or browser tab.

- `icon_path:` - The path (frontend path) of the directory containing your icons.

- `launch_icon_color:` - Launch icon color (e.g. `#BADA55`).

![it IS charging thankyouverymuch](https://user-images.githubusercontent.com/1299821/62975899-c29d6480-be1b-11e9-9b6b-9d160ef8b439.jpg)

---
<a href="https://www.buymeacoffee.com/uqD6KHCdJ" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
