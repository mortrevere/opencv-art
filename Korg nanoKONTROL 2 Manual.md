# Korg nanoKONTROL 2 Manual

The HHDDMMII natively supports the Korg nanoKONTROL 2 as a MIDI controller. Here are the key bindings : 

## Nomenclature
- Numbers are there to identify which slice we are referring to (1 to 8).
- S/M/R are buttons labeled "S", "M" or "R".
- F is for fader
- K is for knob


## Globals

REC : wipeout 
PLAY : on/off HDMI feedback
CYCLE : toggle global filter 
SET + CYCLE : reset global filter settings to defaults
F8 : amount of input in the HDMI feedback loop

### Engines control
S8 : generators on/off
M8 : transformers on/off
R8 : wipers on/off

S6 : previous generator
M6 : previous transformer
R6 : previous wiper

S7 : next generator
M7 : next transformer
R7 : next wiper


### Global filter
The global filter is active all the time. Its configuration can be edited while "CYCLE" is ON. In that case :
- K1 : Contrast
- K2 : Brightness 
- K3 : Saturation
- K4 : Hue (original colors on min and max values)
- K5 : N/A
- K6 : Blue
- K7 : Green
- K8 : Red

> All other buttons and faders are unaffected and can be used normally while the global filter is ON (CYCLE light up)
> The global filter can be reset to its default values with SET + CYCLE while CYCLE is ON




R1 : send reset to current generator (calls reset())
F1 : generator's continuous parameter (CP) #1
K1 : generator's CP #2
F2 : generator's CP #3
K2 : generator's CP #4