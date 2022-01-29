# Tools to communicate with a PeakTech 1255 digital storage oscilloscope

**Note:** Use these tools at your own risk! They have been reverse engineered by looking at network traffic of official PeakScope tools.

**Note:** They have only been tested against a PeakTech 1255, no idea what they'll do to other models.

These tools communicate with the oscilloscope via LAN. You'll need to know the LAN IP address and port number used by the scope. It can be configured in the Utility -> LAN Set menu. Note that a reset is required to apply changes there.

## Capturing the current screen

Assuming the DSO is at IP address 192.168.1.2:

```console
$ python3 capture.py 192.168.1.2 outfile.bin
```

This will capture the currently displayed waveform is a binary dump (with some headers) in `outfile.bin`, overwriting any file without asking. It connects via port 3000 by default, can be overridden using `--port`.

## Show metadata of a screen capture

```console
$ python3 meta.py outfile.bin
outfile.bin
  <peakscope.Bin #chs=1 serial=b'P12551512061'>
  <peakscope.ChannelData 'CH1' 100000ns/div 1000mV/div yshift=+0.00div #samples=3040>
```

This dump contains only a single channel, because I was displaying only a singe channel.

## Plot the dump using matplotlib

```console
$ python3 plot.py outfile.bin
```

This opens a matplotlib GUI with the default provider, rendering the waveform(s) as displayed on the scope.
