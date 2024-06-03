## Deploying
The workflows are currently not working so here's the manual method:

+ Bump the version to match the tag:
```python
bumpversion --current-version 0.1.3 patch pcm/metadata_template.json
```
+ Make the tag
+ Run the build script
```sh
python3 pcm/build.py
```
+ 
## Acknowledgements
+ KiCAD PCM Packaging: Fully based off of (https://github.com/sparkfun/SparkFun_KiCad_Panelizer).
