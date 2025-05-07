conda create --name qrmine python=3.11
conda activate qrmine

conda install conda-forge::uv
uv pip install ini2toml
ini2toml setup.cfg -o pyproject.toml
uv pip install -e .
python -m spacy download en_core_web_sm



pip3 install torch==2.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html