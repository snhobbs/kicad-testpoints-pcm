# KiCAD Test Points
This plugin generates a JigApp compatible test point report for generating bed-of-nails
testers.

This plugin is similar to the command line tool [kicad-testpoints](https://github.com/TheJigsApp/kicad-testpoints) except it can be used entirely within the KiCAD user interface (no terminals required).

## Use
Any pad can be set as a test point. 
Select the pad and edit it's properties. 
Set the 'Fabrication property' drop-down to 'Test point pad'.

![Setting the fabrication property](pad-properties-window.png)

Run the plugin, select the output file and confirm.

![Test Point Report Window](test-point-report-window.png)

The plugin pulls creates the report as a csv.

![Test Point Report CSV](test-point-report.png)

## Acknowledgements
+ KiCAD PCM Packaging: Fully based off of (https://github.com/sparkfun/SparkFun_KiCad_Panelizer).
