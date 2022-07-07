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

## Steps to test this project

1.- the heroku url of this project is
https://clicoh-alex.herokuapp.com

2.- Import the postman collection clicoh_collection.json and clicoh_environment.json

3.- Authentication:
postman collections -> users folder -> login request -> obtain the jwt token(this is automatically loaded on the postman environment and is able on the others requests.)

4.- Test all the endpoints availables on the products and ecommerce folders
