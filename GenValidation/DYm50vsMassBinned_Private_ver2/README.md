# Plotter
---
### Requirements
Plotter use python3-root, please confirm your system can use:
```
python3
import ROOT
exit()
```
---
### Quick Start
Check example.py to see how the plotter works. I have put the test samples in ExampleSamples directory.
```
GITHUB=$(Your github account)
git clone https://github.com/$GITHUB/Plotter.git

python3 example.py
```
The code will make example plots in ExamplePlots directory. If you set many inclusive samples in
files\_incl list, than it will also draw the lines and ratios for those.

---
### How to
To make the code more flexible, I haven't automized the codes for getting histograms. It is hard to know the directory structure of TFiles so user should manage to get the histograms by hands. Also, normalization is not supported in the code side. User should scale the histogram if one wants to. Please see example.py to see how it works.

Basic settings are defined in PlotterBase.py

Extra settings are defined in $CHILDCLASS.py. 

You can change some settings in $CHILDCLASS.py for your purposes. For the example in Quick Start, it used InclAndStitched.py

To make several observalbles at one time, it is convinient to declare the parameters in some place. I defined the parameters in Parameters/$PARAMETER.py. The plotter will use cvs\_params, hist\_params and info\_params to make the full plot. In the Quick Start, the code used Parameters/examples\_params.py.
