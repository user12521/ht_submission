# Readme

# to run this on your machine, clone this repository into a directory and then
do the following:

cd ht_submission
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=ht_project.settings
pytest
python3 manage.py runserver


Q: Why do a Django backend without any models?
A: I was originally planning on doing caching of the API results, but then I
realized that the better design decision would be to store or cache all of the
relevant information about the property at the place in the codebase where it
is all accumulated/brought together.  In such a 'thin' scenario, a more
lightweight framework like Flask would probably be a superior choice.

Q: Mocked up API responses?
A: In ht_submission/wrap_app/tests/wrap_app/test_views.py I mock up both septic
and non-septic API responses.  You can additionally see some responses in the
browser by uncommenting line 44 in /ht_submission/wrap_app/views.py.

Q: Security, scalability, maintainability?
A: As far as security goes, this wrapper would ideally be a microservice
running on an internal network, and only allow requests from certain white-
listed IP addresses, and/or requiring a strong API key in the HTTP request.  I
am not the most knowledgeable on scaling things out massively, but if this
grew to have lots of demand, adding in a PostgreSQL/RDS backend would not be
all that difficult.  As far as maintainability goes, I tried to write clear
code that largely conforms to PEP8 and is well-commented, and use generally
followed traditions in mapping out the code in the django project.  I also
developed this in a test-driven manner, and the tests can be easily modified or
extended for any needed maintenance.  Some directories should have been named
differently but I am leaving them as is, in the interest of time.

Q: Suggested "Next Steps"?
A: Add in gunicorn as the webserver so that this can be ran from a more robust
piece of server software, add strong secret values for the superuser.  Put this
into a Docker container to make deployment very straightforward. Build out a
database backend for caching of results from the HouseCanary API.  Potentially
add in access control, and require user-specific API keys in order to access
this API, and potentially add in allowing POST requests, if that is more
amenable to the consuming software system.  Could also log accesses to this
API for later audit, if this were considered a sensitive piece of data.  This
could potentially be built into an AWS Lambda function but that seems like
overkill to me.







