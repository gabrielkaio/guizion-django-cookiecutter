# {{cookiecutter.project_name}} Back-end implementation

## Guide for installation in Ubuntu 16
### Commands:
RUN:
``` bash
docker-compose up -d
```

Make Migrations:
``` bash
docker-compose run --rm django python ./manage.py makemigrations
```

Migrate:
``` bash
docker-compose run --rm django python ./manage.py migrate
```

## Server Specifications
This server uses Python with Django Framework.

The code follow the Google Python Development Guidelines with can access [here](https://google.github.io/styleguide/pyguide.html)


## Check pylint
```bash
({{cookiecutter.virtual_env_name}}) $: fab check_pylint
```

## Generate the docs
```bash
({{cookiecutter.virtual_env_name}}) $: fab update_the_docs
```
