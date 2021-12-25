# bcoin
This project is a backend API for an associated Discord bot, bcoin-trader. It lets Discord users join and participant in a super serious, highly secure, definetely real crypto economy, trading in the hottest new coin, BCOIN. The B could stand for literally anything and definitely isn't one of my friends. 

Note: This project is *definitely* not secure, well-tested, etc. It was hacked together quickly and probably won't ever be maintained. You have been warned. 

## Tech
This project is built on [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/), both of which are pretty dope and let me write this super fast. The API runs inside a container in a `docker-compose` stack with a [Postgres](https://www.postgresql.org/) DB keeping track of everything. Oh no, wait, I meant to say *iT rUnS oN tHe BlOcKcHaIn.* 

## Configuration
Configuration values are loaded into env vars from a .env file. See [.env.template](.env.template) for an example. The configuration values are as follows:

| Config | Description |
| ------ | ----------- |
| POSTGRES_USER | The user to create for the Postgres DB. The DB will get the same name as this user. |
| POSTGRES_PASSWORD | The password for the DB user. |
| PGADMIN_DEFAULT_EMAIL | The email to use to log in to the pgAdmin console. |
| PGADMIN_DEFAULT_PASSWORD | The password to log in to the pgAdmin console. |
| STARTING_AMOUNT | The amount of bcoin each normal user will receive upon creating a wallet. |
| COOL_GUYS | Comma-separated list of Discord users (with their # identifier too) that should be considered 'cool.' |
| COOL_GUY_AMOUNT | The amount of bcoin each cool guy will receive upon creating a wallet. |

## Tests
Lol maybe someday

## Running
This one's easy: 
```
docker-compose up
```

## Documentation
Django Rest Framework provides a browsable API at `/` and there's a Swagger version at `/swagger-ui/`. 
