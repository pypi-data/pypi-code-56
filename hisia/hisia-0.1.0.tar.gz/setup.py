# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hisia', 'hisia.models']

package_data = \
{'': ['*'], 'hisia': ['data/*', 'visualization/*']}

install_requires = \
['dill==0.3.1.1',
 'lemmy>=2.1.0,<3.0.0',
 'loguru>=0.5.0,<0.6.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'scikit-learn==0.23.1']

setup_kwargs = {
    'name': 'hisia',
    'version': '0.1.0',
    'description': 'A Danish sentiment analysis using scikit-learn',
    'long_description': "Hisia\n==============================\n\n:blush: :smiley: :relaxed: :yum: :wink: :smirk: :flushed: :worried: :frowning: :triumph: :disappointed: :angry: :persevere: :confounded: :shit: \n\n\nA Danish sentiment analyzer using scikit-learn LogisticRegression\n\n![hisia cover](cover_image.png)\n\n```python\nfrom hisia import Hisia\n\nnegative_joe = Hisia('Det er simpelthen ikke okay :(')\nnegative_joe.sentiment\n# Sentiment(sentiment='negative', positive_probability=0.01, negative_probability=0.99)\nnegative_joe.explain\n# {'decision': -2.762615727464413, \n# 'intercept': 0.9959111721097562, \n# 'features': {:(', -4.334440323513933),\n#               ('ikke', -3.425370797679455), \n#               ('simpelthen ikke', -1.6951652194361089),\n#               ('simpelthen', -2.702688329340911)}\n# }\n\npositive_gro = Hisia('Det var ikke dårligt')\npositive_gro\n# Sentiment(sentiment=positive, positive_probability=0.707, negative_probability=0.293)\npositive_gro.explain\n# {'decision': 0.8791611359368057, \n# 'intercept': 0.9959111721097562, \n# 'features': {('ikke dårlig', 5.141224438943983), \n#              ('dårlig', -9.311879340739669), \n#              ('ikke', -3.425370797679455)}\n# }\n```\n### Hisia (Emotions)\n_Hisia_ is a Swahili word for emotion/feeling. My initial thought was to call it _Følelser_, a Danish word for feeling but it was just not right. As a Tanzanian, I went with Swahili as it was much more of a package name I would like to install. :) `pip install hisia`\n\n### Data and Models Used in Hisia\n\n**Data:** 2016 TrustPilot's 254,464 Danish reviews' body and stars and [8 fake reviews]*20 see notes for explanation.<br>\n\n**Models**<br>\nHisia, _LogisticRegression_ with SAGA, a variant of Stochastic Average Gradient (SAG) as a solver, L2 penalty was select for the base model. Test score **accuracy is ca. 93%** and **recall of 93%**. SAGA is a faster solver for large datasets (rows and columns wise). As stochastic gradient, the memory of the previous gradient is incorporated/feed-forward current epoch. This allows a faster convergence rate. Seeds: 42 in data split of 80% training, 20% test, and 42 in the model used for reproducibility. Check notebooks for other parameters.\n\nHisiaTrain, _SGDClassifier_, Stochastic Gradient Descent learner with smooth loss 'modified_huber as loss function and L2 penalty. Test score **accuracy 94%** and **recall of 94%**. SGDClassifier was select because of partial_fit. It allows batch/online training.\n\n**Note:** This score reflects models in regards to TrustPilot reviews style of writing.<b>\n >8*10 fake reviews. TrustPilot reviews are directed towards products and services. A word like 'elsker'(love) or 'hader'(hate) were rare. To make sure the model learns such relationship, I added 8 reviews and duplicated them 20 times. These new sentences did not increase or decrease the model accuracy but correctly added the coefficient of the words love, hate and not bad (ikke dårligt). \n\nNotebook folder contains model_train notebook as a playground to reproduce the scores and also explore what the model has learned.\n\n:warning: Running `from hisia import Hisia` will create a directory `hisia` and move with `model/base_model.pkl` and `data/stops.pkl` in it on the current directory. Until now, I cannot figure out how I can package this library with `poetry` and direct to correct location.\n\nFeatures\n--------\n- Sentiment analysis\n- Sentiment explainer\n- Sentiment reinforcement learning (Coming Soon)\n- Sentiment retrainer (Coming Soon)\n\n\n\nProject Organization\n------------\n\n    ├── LICENSE\n    ├── README.md         \n    │\n    ├── notebooks          <-  Jupyter notebook. Reproduce the results, and show model explanations\n    │   └── model_training.ipynb\n    │   └── helpers.py          \n    │                         \n    │\n    ├── hisia              <-   Source code for use in this project.\n    │\xa0\xa0 ├── __init__.py    <-   Makes hisia a Python module\n    │\xa0\xa0 ├── hisia.py       <-   hisia a sentiment predictor and explainer\n    │   │\n    │\xa0\xa0 ├── data           <-  Path to training and validating dataset and stopwords: data folder is inside hisia for retrain\n    │\xa0\xa0 │\xa0\xa0 └── data.json\n    │   │   └── data_custom.json\n    │   │   └── stops.pkl\n    │   │\n    │\xa0\xa0 ├── models         <-  Helpers, frozen model, models trainer\n    │   │   │                 \n    │\xa0\xa0 │\xa0\xa0 ├── base_model.pkl\n    │\xa0\xa0 │\xa0\xa0 ├── helpers.py\n    │\xa0\xa0 │\xa0\xa0 └── train_model.py\n    │   │\n    │\xa0\xa0 └── visualization  <-  Results oriented visualizations\n    │\xa0\xa0     └── ROC.png\n    │\xa0\xa0     └── ROC_test.png\n    │\n    ├── tests              <-   Path to tests to check models accurance, datatypes, scikit-learn version\n    │\xa0\xa0 ├── __init__.py\n    │\xa0\xa0 ├── conftest.py\n    │   ├── test_basemodel_results.py\n    │\xa0\xa0 ├── test_data.py\n    │   ├── test_scikit_version.py\n    │\xa0\xa0 ├── test_tokenizer.py  \n    │\n    │\n    └── tox.ini            <- tox file to trains base models and run pytests\n\n\n--------\n# Retrain and Test: For Developers\nComing Soon\n",
    'author': 'Prayson W. Daniel',
    'author_email': 'praysonwilfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Proteusiq/hisia',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
