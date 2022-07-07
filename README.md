# clicoh-django


### Local environment
Create user
```bash
python manage.py createsuperuser
email: user@clicoh.com
password: clicoh123@
```


## Heroku

Make deploy
```bash
git push heroku main
```

Create user
```bash
heroku run python manage.py createsuperuser
```

Run migrations
```bash
heroku run python manage.py migrate
```