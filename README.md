# Photo Frame

Just a little python script to do a full screen slideshow of images. Mainly intended for use with a Raspberry Pi to make a homebrew Digital Photo Frame.

Run it with 

```
python3 photo_frame.py -p path/to/imgs/dir
```

## Setup

You probably want to force your display to be always-on. Do this by disabling screen-blanking (should be available in `raspi-config`).

A bash launcher script is included to auto-start the photo-viewer on boot. This script expects an environment variable `PHOTO_DIR` that contains the directory of photos you want in your slideshow.

To autostart a GUI app in a Raspberry Pi on boot, the best thing I've found is to add a boot script line to `/home/pi/.config/lxsession/LXDE-pi/autostart`. If you use the `launcher.sh` script here, be sure you take care of the `PHOTO_DIR` environment variable properly.
