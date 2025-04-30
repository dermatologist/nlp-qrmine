conda create --name qrmine python=3.11
conda activate qrmine

conda install conda-forge::uv
uv pip install ini2toml
ini2toml setup.cfg -o pyproject.toml
uv pip install pandas matplotlib click scikit-learn imbalanced-learn vaderSentiment xgboost mlxtend spacy textacy tensorflow==2.13.1 tensorflow-io-gcs-filesystem==0.31.0 pytest tox
python -m spacy download en_core_web_sm