We use dj-database-url, so something like that should be used:
    $ export DATABASE_URL="postgres://postgres:password@localhost/formidabel"

# Heroku deploy:
    * git subtree push --prefix formidabel heroku master # Because project root is in the formidabel subdirectory 

# Db copy to Heroku
    * /usr/local/bin/pg_dump -Fc --no-acl --no-owner -h localhost -U postgres formidabel > formidabel.dump
    * Copy to an URL-accessible location (Dropbox?)
    * heroku pgbackups:restore DATABASE 'https://dl.dropbox.com/u/31240058/formidabel.dump'
