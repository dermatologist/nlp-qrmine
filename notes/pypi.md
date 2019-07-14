
## Upload

```
pip install twine
twine upload dist/*

```

## Readme MD

* ADD long-description-content-type = text/markdown

```buildoutcfg
long-description = file: README.md
long-description-content-type = text/markdown

```

## Beautify Readme MD

* Link images to same raw file
* Remove emojis :xxx: from MD text
* Installation instructions


## Markdown extension for 

```bash
pip install pyscaffoldext-markdown
putup gtcode -l none  -d "GT Coding script" -u https://nuchange.ca --travis --markdown
```