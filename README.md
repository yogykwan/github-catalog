# github-catalog
fsnd - a website made up of categorized github repositories and user oauth system, where users can manage their own categories and items.

## Setup

1. setup vagrant - `vagrant up --provision`
2. ssh vagrant - `vagrant ssh`
3. enter workdir - `cd /vagrant/catalog`
4. export secrets - `source export_secrets.sh`
5. create db - `python database_setup.py`
6. inject data - `python database_inject.py`
7. start server - `python catalog.py`
8. browse - `http://localhost:5000`

## Usage

1. Users can login(indirect signup) via GitHub OAuth2.
2. Logged in users can new category(name,description) and item(name,url,highlight).
3. Category owner can edit or delete his category and item in it.
4. Item owner can edit or delete his item.
5. Get json data through API endpoints.
6. Flashing message will shine after actions login/logout/new/edit/delete.
