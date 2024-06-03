## Deploying
The workflows are currently not working so here's the manual method:

+ Bump the version to match the tag:
```python
bumpversion --current-version 0.1.3 patch pcm/metadata_template.json kicadtestpoints/resource/_version.py
```
+ Make the tag
+ Run the build script
```sh
python3 pcm/build.py
```
+ This puts our new PCM compatible zip in /build which we can add as an asset to the release
+ When uploaded this appears as:
https://github.com/TheJigsApp/kicad-testpoints-pcm/releases/download/0.1.4/kicadtestpoints-0.1.4-pcm.zip
which matches the metadata.json so its fine.


## Acknowledgements
+ KiCAD PCM Packaging: Fully based off of (https://github.com/sparkfun/SparkFun_KiCad_Panelizer).
