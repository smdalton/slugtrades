#!/usr/bin/env bash
#!/usr/bin/env bash

pip3 install virtualenv
python3 -m virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
