#!/bin/bash	
# chmod +x code-format.sh
# ./code-format.sh

function logging() {	
  echo -e "\033[0;32m$1\033[0m"	
}	
function whereIam() {	
  echo -e "@ \033[07m`pwd`\033[0m"	
}	

MODULE_DIRNAME="form_auto_fill_in"	
HERE=$(cd $(dirname $0);pwd)	

logging "cd $HERE"	
cd $HERE	
whereIam

# flake8
logging "poetry run flake8 ${MODULE_DIRNAME} --count --select=E9,F63,F7,F82 --show-source --statistics"	
poetry run flake8 $MODULE_DIRNAME --count --select=E9,F63,F7,F82 --show-source --statistics
# isort
logging "poetry run isort ${MODULE_DIRNAME}"
poetry run isort $MODULE_DIRNAME
# black
logging "poetry run black ${MODULE_DIRNAME}"
poetry run black $MODULE_DIRNAME
