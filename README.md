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

Using a FAT partition for scripts
------------

Keeping scripts in a regular folder is not quite convenient to update for the novice as an SSH connector or EXT4 support is needed to update the script. The current version of the script will try to locate a mounted FAT partition. And use that partition as the script path. So whenever you need to update the script, just take off the microSD card, put it in any computer no matter what OS you use. And you can update the content. 

In order to make an automatically mounted FAT partition, we can change the partitions in a Linux computer, and configure the fstab for the automatic mount.

GParted tool is quite handy to change the partitions, just unmount any partitions from the card on a computer, shrink the main partition, and add a primary FAT16 partition in the unallocated space. Once you get the FAT partition, it will be visible on all computers.

After you create the FAT partition, put the card in Nano Pi, check partitions with
```lsblk -P -f -p```, and get the device name such as ```/dev/mmcblk0p3```

Create a mounting point with ```mkdir /home/pi/fatDisk``` 

And you can try to mount with ```sudo mount /dev/mmcblk0p3 /home/pi/fatDisk```

Then edit ```/etc/fstab``` for automatic mount with ```sudo nano /etc/fstab```, add entry such as: ```/dev/mmcblk0p3    /home/pi/fatDisk vfat rw,dev,auto,async,users,exec,umask=0000,uid=1000,gid=1000 0 0```

Reboot and check if the files are there with ```ls -al /home/pi/fatDisk```. They should be all 777 permission.

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
