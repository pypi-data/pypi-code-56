# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gino_admin', 'gino_admin.routes']

package_data = \
{'': ['*'], 'gino_admin': ['static/*', 'templates/*', 'templates/modals/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy-Utils==0.36.5',
 'Sanic-Jinja2>=0.7.5,<0.8.0',
 'Sanic>=19.12.2,<20.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'expiring_dict>=1.1.0,<2.0.0',
 'gino-sanic>=0.1.0,<0.2.0',
 'gino>=1.0.0,<2.0.0',
 'passlib>=1.7.2,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'requests_html>=0.10.0,<0.11.0',
 'sanic-auth>=0.2.0,<0.3.0',
 'sanic-jwt>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['gino-admin = gino_admin.cli:cli']}

setup_kwargs = {
    'name': 'gino-admin',
    'version': '0.0.11',
    'description': 'Admin Panel for PostgreSQL DB with Gino ORM',
    'long_description': 'gino-admin\n----------\nDocs in process: `Gino-Admin docs`_\n\nPlay with Demo (current master 0.0.11a2): `>>>> Gino-Admin demo <<<<`_\n\n.. _Gino-Admin docs: https://gino-admin.readthedocs.io/en/latest/ui_screens.html\n\n\n|badge1| |badge3| |badge2| \n\n.. |badge1| image:: https://img.shields.io/pypi/v/gino_admin \n.. |badge2| image:: https://img.shields.io/pypi/l/gino_admin\n.. |badge3| image:: https://img.shields.io/pypi/pyversions/gino_admin\n\n\nAdmin Panel for PostgreSQL DB with Gino ORM and Sanic\n\n.. image:: https://raw.githubusercontent.com/xnuinside/gino-admin/master/docs/img/table_view_new.png\n  :width: 600\n  :alt: Table view\n\n\nSupported features\n--------------------\n\n- Auth by login/pass with cookie check\n- Create(Add new) item by one for the Model\n- Search/sort in tables\n- Upload/export data from/to CSV\n- Delete all rows/per element\n- Copy existed element (data table row)\n- Edit existed data (table row)\n- SQL-Runner (execute SQL-queries)\n- Presets: Define order and Load to DB bunch of CSV-files\n- Drop DB (Full clean up behavior: Drop tables & Recreate)\n- Deepcopy element (recursive copy all rows/objects that depend on chosen as ForeignKey)\n- Composite CSV: Load multiple relative tables in one CSV-file\n\n\nTODO:\n\n- Select multiple for delete/copy\n- Edit multiple items (?)\n- Roles & User store in DB\n- Filters in Table\'s columns\n- History logs on changes (log for admin panel actions)\n- Add possible to add new Presets from GUI\n\nVersion 0.0.11 Updates\n----------------------\n\n1. Added possibility to define custom route to Gino Admin Panel. With \'route=\' config setting\nBy default, used \'/admin\' route\n\n2. Added Demo Panel  `Gino-Admin demo`_ - you can log in and play with it. Login & pass - admin / 1234\nIf you don\'t see any data in UI maybe somebody before you cleaned it - go to Presets and load one of the data presets.\n\n.. _Gino-Admin demo: http://xnu-in.space/gino_admin_demo\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/logo/demo.png\n  :width: 250\n  :alt: Load Presets\n\n3. Fixed minors issues: 1)floats now displayed with fixed number of symbols. Parameter can be changed with config param `round_number=`.\n2) now file upload fill not raise error if no file was chosen\n\n4. Deepcopy now ask id - you can use auto-generated or define own id to \'deepcopy object\'\n\n![Table view](docs/img/deepcopy.png)\n\nFull changelog for all versions see in [CHANGELOG.txt](CHANGELOG.txt)\n\n\nHow to install\n--------------\n\n.. code-block:: python\n    \n    pip install gino-admin==0.0.11a2\n    \n\n\nVersion 0.0.11 Updates (current master, not released):\n------------------------------------------------------\n1. Added possibility to define custom route to Gino Admin Panel. With \'route=\' config setting\nBy default, used \'/admin\' route\n\n2. Added Demo Panel  `>>>> Gino-Admin demo <<<<`_ - you can log in and play with it. Login & pass - admin / 1234\nIf you don\'t see any data in UI maybe somebody before you cleaned it - go to Presets and load one of the data presets.\n\n.. _>>>> Gino-Admin demo <<<<: http://xnu-in.space/gino_admin_demo\n\n3. Fixed minors issues: floats now displayed with fixed number of symbols. Parameter can be changed with config param `round_number=`,\n\n4. Updated docs\n\n\nVersion 0.0.10 Updates:\n-----------------------\n1. GinoAdmin Config moved to Pydantic.\nAdded possible to send any properties to config with config dict. Example:\n.. code-block:: python\n\n    add_admin_panel(\n        app,\n        db,\n        [User, Place, City, GiftCard, Country, Item],\n        # any Gino Admin Config params you can pass as named params\n        custom_hash_method=custom_hash_method,\n        presets_folder=os.path.join(current_path, "csv_to_upload"),\n        name=\'Base Example\')\n\n\n2. Added Config param \'name\' - this is a name, that will be showed in header near menu.\nBy Default it is display "Sanic-Gino Admin Panel", now you can change it to your header.\n\n3. UI updates: Gino Admin Panel version now showed in UI footer, Login page now more presentable,\nchanged index page of Admin Panel, now it presented main feature.\n\n4. Initialised first project\'s docs\n\n5. Edit/Delete now take object\'s unique key as argument and stop fall if in key was \'/\' symbol\n\n6. Added param \'csv_update_existed\' in Config. By default \'csv_update_existed = True\'. This mean if you upload CSV with rows with unique keys, that already exist in DB - it will update all fields with values from CSV.\nYou can turn off it with set \'csv_update_existed = False\'.\n\n\nHow to use\n----------\n\nYou can find several code examples in \'examples\' folder.\n\n\nRun Admin Panel from Command line\n#################################\n\n**Run Admin Panel from cli**\n\n.. code-block:: python\n\n    gino_admin run #module_name_with_models -d postgresql://%(DB_USER):%(DB_PASSWORD)@%(DB_HOST):%(DB_PORT)/%(DB)\n\n    Optional params:\n        -d --db\n            Expected format: postgresql://%(DB_USER):%(DB_PASSWORD)@%(DB_HOST):%(DB_PORT)/%(DB)\n            Example: postgresql://gino:gino@%gino:5432/gino (based on DB settings in examples/)\n            Notice: DB credentials can be set up as  env variables with \'SANIC_\' prefix\n        -h --host\n        -p --port\n        -c --config Example:  -c "presets_folder=examples/base_example/src/csv_to_upload;some_property=1"\n                    Notice: all fields that not supported in config will be ignored, like \'some_property\' in example\n        --no-auth  Run Admin Panel without Auth in UI\n        -u --user Admin User login & password\n            Expected format: login:password\n            Example: admin:1234\n            Notice: user also can be defined from env variable with \'SANIC_\' prefix - check Auth section example\n\nExample:\n\n.. code-block:: python\n\n    gino-admin run examples/base_example/src/db.py postgresql://gino:gino@%gino:5432/gino -u admin:1234\n\n\nAdd Admin Panel to existed Sanic application as \'/admin\' route\n##############################################################\n\nCreate in your project \'admin.py\' file and use `add_admin_panel` from from gino_admin import add_admin_panel\n\nCode example in:  examples/base_example\nHow to run example in: examples/base_example/how_to_run_example.txt\n\nExample:\n\n.. code-block:: python\n    \n    \n    from from gino_admin import add_admin_panel\n\n\n    # your app code\n\n    \n    add_admin_panel(\n        app, db, [User, Place, City, GiftCard], custom_hash_method=custom_hash_method\n    )\n        \n    \nWhere:\n\n* \'app\' - your Sanic application\n* \'db\' : from gino.ext.sanic import Gino; db = Gino() and\n* [User, Place, City, GiftCard] - list of models that you want to add in Admin Panel to maintain\n* custom_hash_method - optional parameter to define you own hash method to encrypt all \'_hash\' columns of your Models.\n\nIn admin panel _hash fields will be displayed without \'_hash\' prefix and fields values will be  hidden like \'******\'\n\nRun Admin Panel as Standalone Sanic app (if you use different frameworks as main App)\n#####################################################################################\n\nYou can use Gino Admin as stand alone web app. Does not matter what Framework used for your main App.\n\nCode example in:  examples/use_with_any_framework_in_main_app/\nHow to run example in: examples/use_with_any_framework_in_main_app/how_to_run_example.txt\n\n1. In module where you define DB add \'if block\'.\nWe will use Fast API as main App in our example.\n\nWe have db.py where we import Gino as\n\n.. code-block:: python\n\n    from gino.ext.starlette import Gino\n\n    db = Gino(\n        dsn=\'postgresql://gino:gino@localhost:5432/gino\'\n    )\n\nBut if we use this module in Admin Panel we need to have initialisation like this:\n\n.. code-block:: python\n\n    from gino.ext.sanic import Gino\n    db = Gino()\n\nTo get this, we will add some flag and based on this flag module will init db in needed to as way:\n.. code-block:: python\n\n    if os.environ.get(\'GINO_ADMIN\'):\n        from gino.ext.sanic import Gino\n        db = Gino()\n    else:\n        from gino.ext.starlette import Gino\n        db = Gino(dsn=\'postgresql://gino:gino@localhost:5432/gino\')\n\nSo, if now \'db\' used by Gino Admin - we use init for Sanic apps, if not - we use for our Main application Framework\n\nNow, we need to create **admin.py** to run admin panel:\n\n.. code-block:: python\n\n    import os\n\n    from gino_admin import create_admin_app\n\n    os.environ["GINO_ADMIN"] = "1"\n\n    # gino admin uses Sanic as a framework, so you can define most params as environment variables with \'SANIC_\' prefix\n    # in example used this way to define DB credentials & login-password to admin panel\n\n    os.environ["SANIC_DB_HOST"] = "localhost"\n    os.environ["SANIC_DB_DATABASE"] = "gino"\n    os.environ["SANIC_DB_USER"] = "gino"\n    os.environ["SANIC_DB_PASSWORD"] = "gino"\n\n\n    os.environ["SANIC_ADMIN_USER"] = "admin"\n    os.environ["SANIC_ADMIN_PASSWORD"] = "1234"\n\n\n    if __name__ == "__main__":\n        # variable GINO_ADMIN must be set up before import db module, this is why we do import under if __name__\n        import db # noqa E402\n\n        # host & port - will be used to up on them admin app\n        # config - Gino Admin configuration,\n        # that allow set path to presets folder or custom_hash_method, optional parameter\n        # db_models - list of db.Models classes (tables) that you want to see in Admin Panel\n        create_admin_app(host="0.0.0.0", port=5000, db=db.db, db_models=[db.User, db.City, db.GiftCard])\n\n\n\nAll environment variables you can move to define in docker or .env files as you wish, they not needed to be define in \'.py\', this is just for example shortness.\n\n\nPresets\n-------\nLoad multiple CSV to DB in order by one click.\n\n\'Presets\' feature allows to define folder with DB presets described in yml format.\nPresets described that CSV-s files and in that order\n\nCheck also \'example/\' folder.\n\n\nExample:\n\n.. code-block:: python\n\n    name: First Preset\n    description: "Init DB with minimal data"\n    files:\n      users: csv/user.csv\n      gifts: csv/gift.csv\n\n\nCheck examples/base_example/src/csv_to_upload for example with presets files.\n\n\nIn order defined in yml, Gino-Admin will load csv files to models.\n\'files:\' describe that file (right sight) must be loaded to the model (left side).\n\nIn current example: load data from csv/user.csv to Users table, csv/gift.csv to Gifts.\n\nDon\'t forget to setup path to folder with presets like with **\'presets_folder\'** argument.\n\n.. code-block:: python\n\n    ...\n\n    current_path = os.path.dirname(os.path.abspath(__file__))\n\n    add_admin_panel(\n        app,\n        db,\n        [User, Place, City, GiftCard, Country],\n        custom_hash_method=custom_hash_method,\n        presets_folder=os.path.join(current_path, "csv_to_upload"),\n    )\n\nCheck example project for more clearly example.\n\nComposite CSV to Upload\n-----------------------\nDefault upload from CSV allows to load CSV with data per table.\n\nComposite CSV files allow to load data for several tables from one CSV files and don\'t define ForeignKey columns.\nYou can define table from left to right and if previous table contain ForeignKey for the next table when as linked row will be taken value from current or previous row.\nThis allow you to define one time Country and 10 cities for it. If it sounds tricky - check example DB schema and XLS example on google docs.\n\nThis useful if you want to fill DB with related data, for example, User has some GiftCards (ForeignKey - user.id), GiftCard can be spend to pay off for some Order (ForeignKey - gift_card.id).\nSo you have set of data that knit together. If you works on some Demo or POC presentation - it\'s important to keep data consistent, so you want to define \'beautiful data\', it\'s hard if you have 3-4-5 models to define in separate csv.\n\nComposite CSV allow use CSV files with headers with pattern "table_name:column" and also allow to add aliases patterns\n\nCheck \'examples/composite_csv_example\' code to check DB structure.\n\nAnd XLS-table sample in Google Sheets:\n\nhttps://docs.google.com/spreadsheets/d/1ur63acwWExyjWouZ1WEkUxCX73vOcdXzCrEYc7cPhTg/edit?usp=sharing\n\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/composite_csv.png\n  :width: 250\n  :alt: Load Presets\n\n\nClick - Download -> CSV and you will get result, that can be found in **examples/composite_csv_example/src/csv_to_upload**\n\n\nComposite CSV can be loaded manual from any Model\'s Page where exist button \'Upload CSV\' - it does not matter from that model you load.\n\nOr you can define preset with Composite CSV and load it as preset. To use composite CSV you need to define key, that started with \'composite\' word.\n\nExample:\n\n.. code-block:: python\n\n    name: Composite CSV Preset\n    description: "Init DB with data from composite CSV"\n    files:\n      composite_csv: csv/preset_a/users.csv\n\n\'composite_csv: csv/preset_a/users.csv\' can be \'composite_any_key: csv/preset_a/users.csv\'\n\nYou can use multiple composite CSV in one preset.\n\n\nConfig Gino Admin\n------------------\n\nYou can define in config:\n\n* presets_folder: path where stored predefined DB presets\n* custom_hash_method: method that used to hash passwords and other data, that stored as \'_hash\' columns in DB, by default used pbkdf2_sha256.encrypt\n* composite_csv_settings: describe some rules how to parse and load Composite CSV files\n\n\ncomposite_csv_settings\n######################\n\ncomposite_csv_settings allow to define multiple tables as one alias\n\nFor example, in our example project with composite CSV we have 3 huge different categories separated by tables (they have some different columns) - Camps, Education(courses, lessons, colleges and etc.) and Places(Shopping, Restaurants and etc.)\nBut we want to avoid duplicate similar columns 3 times, so we can call those 3 tables by one alias name,\nfor example: \'area\' and some column to understand that exactly this is an \'area\' - capms, educations or places table for this we need to define \'type_column\' we don\'t use in any model column \'type\' so we will use this name for type-column\n\nSo, now let\'s define **composite_csv_settings**\n\n.. code-block:: python\n\n    composite_csv_settings={\n        "area": {"models": (Place, Education, Camp), "type_column": "type"}\n    }\n\nThis mean, when we see in CSV-header \'area\' this is data for one of this 3 models, to identify which of this 3 models - check column with header \'area:type\'.\nIn type column values must be same 1-to-1 as table names.\n\nCheck source code with example: examples/composite_csv_example\n\nAnd table sample for it: https://docs.google.com/spreadsheets/d/1ur63acwWExyjWouZ1WEkUxCX73vOcdXzCrEYc7cPhTg/edit?usp=sharing\n\nYou also can define table name as \'pattern\':\n\n.. code-block:: python\n\n    composite_csv_settings={\n        "area": {"models": (SomeModel, SomeModel2, SomeModel3), "pattern": "*_postfix"}\n    }\n\nThis mean - to understand that this is a DB - take previous table from CSV in row and add \'_postfix\' at the end.\n\n\nDrop DB\n-------\n\nDrop DB feature used for doing full clean up DB - it drop all tables & create them after Drop for all models in Admin Panel.\n\n\nUpload from CSV\n---------------\n\nFiles-samples for example project can be found here: **examples/base_example/src/csv_to_upload**\n\n\nAuthorization\n--------------\n\nRead in doc : `Authorization`_\n\n.. _Authorization: https://gino-admin.readthedocs.io/en/latest/authorization.html\n\n\nLimitations\n-----------\n\nRead in doc : `Limitations`_\n\n.. _Limitations: https://gino-admin.readthedocs.io/en/latest/limitations.html\n\nUI Screens\n----------\n\nIn Docs : `UI Screens`_\n\n.. _UI Screens: https://gino-admin.readthedocs.io/en/latest/ui_screens.html',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/gino-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
