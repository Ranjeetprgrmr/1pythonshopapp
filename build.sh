# exit on error
set -o errexit 

# modify this line as needed for you package manager
pip install -r requirements.txt

# convert static asset files
python manage.py collectstatic --no-input

# apply any outstanding database migrations
python manage.py migrate