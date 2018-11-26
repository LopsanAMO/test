# Grin Test
 [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/096cb959dfa9114a426e#?env%5Bgrin_env%5D=W3sia2V5IjoibG9jYWxfdXJsIiwidmFsdWUiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvIiwiZGVzY3JpcHRpb24iOiIiLCJ0eXBlIjoidGV4dCIsImVuYWJsZWQiOnRydWV9XQ==)


# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Documentation
Once running the project locally go to `http://localhost:8001/` to see the complete documentation, there you will find a dropdown that says API, there you will find all the documentation of the api

# Notes
To make everything work, you must add a valid `GOOGLE_API_KEY` and add it to the file `docker-compose.yml`, without that key, nothing will work

# Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.

Initialize the production server:

```
heroku create places-prod --remote prod && \
    heroku addons:create newrelic:wayne --app places-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app places-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="places-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="places.config" \
        --app places-prod
```

Initialize the qa server:

```
heroku create places-qa --remote qa && \
    heroku addons:create newrelic:wayne --app places-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app places-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="places-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="places.config" \
        --app places-qa
```

Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master
```

You're now ready to continuously ship! ✨ 💅 🛳

