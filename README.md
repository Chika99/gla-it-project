# First Run

1. Create a virtual environment `python3 -m venv <path>`
2. Actavate virtual environment
   - Linux/Mac `source <path>/bin/activate`
   - Windows `<path>\Scripts\activate.bat` or `<path>\Scripts\Activate.ps1`

# Update

1. pull latest code version `git pull`
2. update dependencies `pip install -r requirements.txt`
3. Model modification create migration `python manage.py makemigrations`
4. Application Migration `python manage.py migrate --run-syncdb`
5. Populate the database`python population_script.py`
   - Note that after the previous step, ensure that the parameters `--run-syncdb` are added Make sure the database is created
6. Start the service `django-admin runserver`
   - If it doesn't work, check `DJANGO_SETTINGS_MODULE` environment variable
     - Linux/Mac `export DJANGO_SETTINGS_MODULE=auction.settings`
     - Windows `set DJANGO_SETTINGS_MODULE=auction.settings`
     - or specify at startup `django-admin runserver --settings=auction.settings`
   - If it says the auction module cannot be found, try `python manage.py runserver`
7. test
