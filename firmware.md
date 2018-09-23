# Firmware

## Interfacing with the microcontroller

The E8a emulator which is typically used to program and debug Renesas chips, is rather expensive ($150) for a one-time use.
As an alternative, RS-232 interface can used for basic operations.

Luckily there exists a low-cost (and open-source) [solution](http://people.redhat.com/dj/m32c/),
[developed](http://people.redhat.com/dj/m32c/flash-tool.tar.gz) and [documented](http://people.redhat.com/dj/m32c/flash-guide.pdf) by
DJ Delorie, consisting of programming hardware, called [gR8C](http://www.delorie.com/electronics/gR8C/) and companion flash tools.

### Creating your own gR8C clone

gR8C is essentially a glorified FTDI FT232R board, which means that in theory any existing FT232R module would do. However some of the
hardware requirements will narrow down the viability of some the possible options:
* Access to CBUS2 pin on the FT232R chip (pin 13), which is used for bitbanging the MODE pin
* Access to DTR signal, which is used for resetting the chip via nRESET pin.
* It should have a mode for using 3.3V logic!

DTR signal is exposed on most boards, a lot of boards also have a jumper or switch to choose between 3.3V or 5V, however CBUS2 might
require soldering directly to the pin of the chip if it even can be accessed. Looking at Aliexpress, there are
[some modules](https://www.aliexpress.com/af/ft232r.html) which cost only a couple of dollars and the necessary connections exposed as
holes, onto which pin headers can be soldered without too much of a difficulty.

The backside of these inexpensive Aliexpress boards looks like this:
![](https://i.imgur.com/BuPXJqK.jpg)

I used [ITEAD Foca](https://www.itead.cc/wiki/Foca) because this was what I had handy, it has a DTR signal exposed
and I only needed to solder a tiny wire on the pin 13, which was achieved easily using small diameter leaded solder and generous amount of flux.

Once you have the hardware with CBUS2 and DTR pin exposed, you'll need [FT_PROG](https://www.ftdichip.com/Support/Utilities.htm#FT_PROG)
software to reconfigure the board. First make a backup of the current settings by clicking the save icon in case you want to later
revert to the original configuration.

Changes required are as follows:
* USB String Descriptors -> Product Description, set to: `FT232R - R8C`
* Hardware Specific -> Invert RS232 Signals -> Invert DTR#, tick the checkbox
* Hardware Specific -> IO Controls -> C2, set to I/O MODE
* Hardware Specific -> IO Controls -> C3, set to I/O MODE (could be optional)
* Hardware Specific -> IO Controls -> C4, set to PWREN# (could be optional)

To program the changes, click the lightning bolt icon, or select DEVICES -> Program from the menu.

Later you may just open your saved file and program that directly to revert the changes you made.

### Setting up the flashing utilities

I used a computer with Ubuntu 18.04 for the utilitites. You may compile the utilities on Windows too, however Linux may be more reliable
in terms of the expected results.

First you need to install some dependencies required to compile the flash utilities:
```sh
sudo apt update
sudo apt install build-essential libftdi-dev
```

Then download and extract the source code for [tools](http://people.redhat.com/dj/m32c/flash-tool.tar.gz).

The tools seem to lack a straightforward way of dumping the device's memory into a file, however we can fix it by adding a few
lines of code.

Open `mflash.c` file in a text editor and find the following part:
```c
      if (save_data_flash)
	{
	  byte buf[256];
	  int i;

	  for (i=data_flash_start; i<data_flash_end; i+=256)
	    {
	      read_page (i >> 8, buf);
	      progmem_puts (i, buf, 256);
	    }
	}
```

Replace it with the following:
```c
      FILE *outputFile = fopen("firmware_dump.bin", "w");
      if (outputFile == NULL)
      {
          printf("Error opening file!\n");
          exit(1);
      }

      if (save_data_flash)
	{
	  byte buf[256];
	  int i;

	  for (i=data_flash_start; i<data_flash_end; i+=256)
	    {
	      read_page (i >> 8, buf);
	      progmem_puts (i, buf, 256);
	      fwrite(buf, 1, 256, outputFile);
	    }
	}
  
	fclose(outputFile);
```

Save and close the editor.

Then in Terminal, inside the directory of the source code, you'll need to simply run
```bash
make
```
which should build all the necessary components. You may test if everything works, by executing:
```bash
./uflash -h
```
You should be greeted with the help text for that program.

### Making necessary electrical connections:

1) Switch off the main power from the ECL Comfort 110 as we will be feeding the board using our own power source.
2) Set your FT232R module to 3.3V.
3) Follow the table below to make the connections using some 0.1" jumper wires:

<table>
  <tr>
    <td>2</td>
    <td>4</td>
    <td>6</td>
  </tr>
  <tr>
    <td>TXD</td>
    <td>+3.3V</td>
    <td>GND</td>
  </tr>
  <tr>
    <td>RXD</td>
    <td>nRESET</td>
    <td>MODE</td>
  </tr>
  <tr>
    <td>1*</td>
    <td>3</td>
    <td>5</td>
  </tr>
</table>

Pin 1 is the bottom left one when viewed directly the front side of the board and can be distinguished by the square pad, which is
visible from the behind of the board.

TXD and RXD connections should be inverted between two sides (FT232R-s TXD connects to RXD on the board and vice-versa)

nRESET should be connected to DTR

MODE should be connected to CBUS2

Double-check your connections and then insert the module to your computer.

### Using the flashing software to make a backup of the existing ROM

Now it should be possible to extract the contents of the chip's memory. We can do it by entering the following command:
```bash
touch empty.txt
sudo ./uflash -qt -F 0,FFFFF empty.txt
```

The option `q` will stop the program after querying the information of the board, seeing chip as `unknown` is normal. In our case
the program will exit when the task for the option `F` is done.

The option `t` enables trace messages, which show us some progress when it is interacting with the chip.

The option `F` will read in the existing flash and saves it in the memory of the program and also due to the modifications made by us,
saves it to the file. `0` and `FFFFF` designates that we want the whole addressable space of the memory, not just a part of it.

The file `empty.txt` needs to be there or else the program will exit prematurely. It will have no effect on the chip with the options we
are currently using.

The process should take only a few minutes.

Example output:
```
saving data flash: 0 to 100000, size 100000
chip 1 cnvss -1
sync
Version = "VER.1.00"  Chip = R8C
checking status
done checking status
read page 000000--
read page 000001--
read page 000002--
read page 000003--
read page 000004--
read page 000005--
read page 000006--
read page 000007--
read page 000008--
...
read page 000ff1--
read page 000ff2--
read page 000ff3--
read page 000ff4--
read page 000ff5--
read page 000ff6--
read page 000ff7--
read page 000ff8--
read page 000ff9--
read page 000ffa--
read page 000ffb--
read page 000ffc--
read page 000ffd--
read page 000ffe--
read page 000fff--
```

If the program exits, we should be left with a file called `firmware_dump.bin` which contains all of the memory of the flash when it was
extracted. You may save that file elsewhere and repeat the last command 2 or 3 times to confirm that the files resulting from the
process are similar enough (since we are also reading in the registers and RAM, they will not be identical, but as long as the differences
are before offset 0x4000, it should be safe to assume that the gR8C clone works and has no issues reading the chip)

