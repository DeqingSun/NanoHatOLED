## **NanoHat OLED**

Script Launcher
------------

![Launcher img](https://github.com/DeqingSun/NanoHatOLED/raw/imageHost/nanoPiHatOptimized.gif)

This is a Python script lists all scripts in `/home/pi/scripts/`. You may use buttons to select and run scripts, and make repetitive tasks easy and intuitive.

To use this script, move `bakebit_nanohat_oled.py` and `scriptrunner.png` into `/root/NanoHatOLED/BakeBit/Software/Python/` where the original script locates. Make sure your new script has execution permission.

Move `scripts` folder into `/home/pi/`

Restart and the script should work.

Increase OLED refresh rate
------------

By default the I2C0 on NanoPi NEO2 is slow, we can change I2C clock speed to 400K to improve it.

`fdtdump /boot/sun50i-h5-nanopi-neo2.dtb`

We can find "i2c@01c2ac00", although we didn't find clock-frequency, but we can still do it!

`sudo fdtput --type u /boot/sun50i-h5-nanopi-neo2.dtb /soc/i2c@01c2ac00 clock-frequency 400000`

check if frequency  is OK

`sudo fdtget --type u /boot/sun50i-h5-nanopi-neo2.dtb /soc/i2c@01c2ac00 clock-frequency `

Original Instruction
------------

Example code of correct use and start for the NanoHat OLED.  

Designed specifically to work with the NanoHat OLED:
http://wiki.friendlyarm.com/wiki/index.php/NanoHat_OLED

Currently supported boards (Plug & Play):
* NanoPi NEO
* NanoPi NEO Air
* NanoPi NEO2
* NanoPi NEO Plus2.

Also support other development board with the i2c interface (Need to manually connect).  


Installation
------------
Execute the following command in the Ubuntu core system:    

```
# git clone https://github.com/friendlyarm/NanoHatOLED.git
# cd NanoHatOLED
# sudo -H ./install.sh
```
The demo will automatically start at the next reboot.  

## License

The MIT License (MIT)
Copyright (C) 2017 FriendlyELEC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
