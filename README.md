# KiCAD Test Points
This plugin generates a JigApp compatible test point report for generating bed-of-nails
testers.

This plugin is similar to the command line tool [kicad-testpoints](https://github.com/TheJigsApp/kicad-testpoints) except it can be used entirely within the KiCAD user interface (no terminals required).

[![Watch the video](https://img.youtube.com/vi/Z7aEWe4d0jE/hqdefault.jpg)](https://www.youtube.com/embed/Z7aEWe4d0jE)

[<img src="https://img.youtube.com/vi/Z7aEWe4d0jE/hqdefault.jpg" width="600" height="300"
/>](https://www.youtube.com/embed/Z7aEWe4d0jE)


## Use
Any pad can be set as a test point. 
Select the pad and edit it's properties. 
Set the 'Fabrication property' drop-down to 'Test point pad'.

![Setting the fabrication property](pad-properties-window.png)

Run the plugin, select the output file and confirm.

![Test Point Report Window](test-point-report-window.png)

The plugin pulls creates the report as a csv.

![Test Point Report CSV](test-point-report.png)

## Links
+ [Blog Post](https://www.thejigsapp.com/blog/2024/06/03/kicad-testpoints-plugin/)
+ [Video Introduction](https://www.youtube.com/watch?v=Z7aEWe4d0jE)

## Acknowledgements
+ KiCAD PCM Packaging: Fully based off of (https://github.com/sparkfun/SparkFun_KiCad_Panelizer).
