# build_files.sh

#!/bin/bash

pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 manage.py collectstatic