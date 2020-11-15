# opencv-art

This is a software / hardware video FX box.

## Context 

With the [beLow art collective](https://below.black), among other things, we play live VJ events.
These performances need at least a video source (usually [Resolume](https://resolume.com/)), and effects. The video output is then displayed on a set of projectors or analog TVs.

However I became bored with the effects available in Resolume, its rigid midi mapping, and I guess I just wanted to build an autonomous system capable of doing the job.
Much like an analog video processor would do with composite signals, this takes [HDMI in over USB](https://www.amazon.fr/DIGITNOW-enregistreur-caméscope-Diffusion-Android-Mac/dp/B0895N9KM5/), and spits a modified image on HDMI.

It's controllable using any MIDI controller, but supports natively the [Korg nanoKONTROL 2](https://www.thomann.de/fr/korg_nanokontrol_2_white.htm). One would have to write a different `config.ini` file to support another controller.

## Architecture

![architecture](doc/archi.png)

The green part is optional, but allows to get feedback about what is going on in the program. It is designed to be used on another device, like a phone or another computer for performances reasons, and also because the main computer in the practical setup is a raspberry pi, without a screen. 
The web UI that connects to the FX engine is accessible in the `UI/` folder, as a HTML page.

## Contributing

It is fairly easy to contribute to this project. It includes a set of filters that just waits to be extended. Creating a filter is simple, and doesn't even require having a midi controller.
However, having one can ease the creative process, as you'll be able to change parameters in real time.

- Copy `allpass.py` (a fitler that does nothing, the default one) to `newfiltername.py`
- Rename the class to `WhateverNameFilter`
- Change the default filter to `WhateverNameFilter` in `config.ini` (under `[misc]` -> `default_filter`). This will use your new filter as the default one when executing the code.
- Launch the application

If you have multiple video inputs (like webcams or HDMI to USB capture cards), you can chose the default input id to use in `config.ini`, under `[misc]` -> `default_input`. Inputs can be listed with `ls /dev/ | grep video`.
