set -o errexit

pip install -r ../requirements.txt 

python mairie/manage.py collectstatic --no-input

python mairie/manage.py migrate

