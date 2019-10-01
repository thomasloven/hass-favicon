favicon
=======

Change the favicon and app icons of your Home Assistant instance

![browser](https://user-images.githubusercontent.com/1299821/62975860-ad283a80-be1b-11e9-836a-d58a1732fb21.png)

# Installation instructions

- Copy the contents of `custom_components/favicon/` to `<your config dir>/custom_components/favicon/`.

- Get some icons

  There are some nice ones available [here](https://github.com/home-assistant/home-assistant-assets/tree/master/Alternates), and you can generate favicons from them using an online tool, such as [this one](https://realfavicongenerator.net/).

- Put your icons in e.g. `<your config dir>/www/favicons/`. Note that `<your config dir>/www/` translates to `/local/` for the Icon path.
Note: If you created `<your config dir>/www/` you need to restart Home Assistant once before any icons will be found.

- Go to your Home Assistant configuration and to Integrations

- Add a "Favicon" integration

- Enter your wanted title and the path to your icons. E.g. `Icon path: /local/favicons/`

- Press submit

- Refresh the page

See readme on github for more info about the icons.

![integration](https://user-images.githubusercontent.com/1299821/65991117-1d068900-e48d-11e9-9002-f2253fafa190.gif)


![iphone](https://user-images.githubusercontent.com/1299821/62975899-c29d6480-be1b-11e9-9b6b-9d160ef8b439.jpg)
