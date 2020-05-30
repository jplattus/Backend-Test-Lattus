
# Cornershop's Backend Test 

## Instalation Instructions

### Pre-requisites
- Redis
- Postgres
- Python 3.6+
- Access to your slack workspace configuration

### Create and config your slack app
1. First [create new app](https://api.slack.com/apps?new_app=1) into your Slack Workspace
2. Go to Features > OAuth & Permissions
3. In Scopes add "chat:write" and "im:write" scopes
4. Install the app using "Install App to Workspace " at the top of the page
5. Check what actions your AppName can do. If ok, then click "Allow" Button 
6. You will be redirected to OAuth & Persmissons page. Copy "Bot User OAuth Access Token" and save it. We have to paste it at SLACK_TOKEN in **secrets.json** file described late in this file.
7. The token should look like this `xoxb-9191919199191-91919199191919-ASDfASdFAsdfASDfasdF`

### Create the #lunch channel and invite the bot
1. In the same workspace you created your app, create a channel (called #lunch for example) and invite the Cornershop team
2. You will need the channel id to paste in **secrets.json** file at SLACK_CHANNEL described later. You can get the channel id using this [tutorial](https://es.wikihow.com/encontrar-el-ID-de-un-canal-en-Slack-en-una-PC-o-Mac)
3. Invite the bot using /invite @botname . Usually called as the app name

### Setup your Django App
1. Create python3 virtual env `python3 -m venv /path/to/your/env/`
2. Cd to your venv and mount in `source bin/activate`
3. Inside your venv dir, clone the repo 
    <pre><code>$ git clone https://github.com/jplattus/Backend-Test-Lattus.git</code></pre>
4. Cd into the repo folder and install pip packages <pre><code>$ pip install -r requirements.txt</code></pre>
5. Create postgresql database 
6. You can use sqlite3 database changing the configuration in **settings.py** file
7. IMPORTANT: create a json file **secrets.json** in your project base directory with this structure
    <pre><code>
    {
        "SECRET_KEY": "3(lfyqkt8o)h&9jpqql#l2g2fbm$arch^mq!$r(3@7tv+c7!-r",
        "DB_USER": "your_database_user",
        "DB_PASSWORD": "your_database_password",
        "SLACK_CHANNEL": "your_slack_channel_id",
        "SLACK_TOKEN": "your_slack_bot_token"
    }
    </code></pre>

8. Make migrations `python manage.py makemigrations`
9. Migrate `python manage.py migrate`
10. Create Nora's user `python manage.py createsuperuser`

You are set.

Run the Django app initialization redis and celery 
    <pre><code>
$ redis-server
$ celery worker -A backend_test_lattus.celery --loglevel=info
$ python manage.py runserver
    </code></pre>

- Running app tests `python manage.py test noraslunch` 
- Running tasks (slack_message) tests `python manage.py test tasks_tests` 

Todo: 
- Improve design
- Implement pagination in MENU LIST
- Functional testing using browser
- Implement removal of formset items in UPDATE MENU


## Test instructions 

This technical test requires the design and implementation (using Django) of a basic management system to coordinate the meal delivery for Cornershop employees.

## Before you begin

You will need to create a private GitHub repository using the information that we provided in this README and invite as collaborators: @varellanov @galitisrael @omenar.
Should you have any technical questions, please contact osvaldo@cornershopapp.com
Tittle of the project: Backend-Test-(Last Name)

## Description

The current process consist of a person (Nora) sending a text message via Whatsapp to all the chilean employees, the message contains today's menu with the different alternatives for lunch. 

> Hola!  
> Dejo el menú de hoy :)
>
> Opción 1: Pastel de choclo, Ensalada y Postre  
> Opción 2. Arroz con nugget de pollo, Ensalada y Postre  
> Opción 3: Arroz con hamburguesa, Ensalada y Postre  
> Opción 4: Ensalada premium de pollo y Postre  
>
> Tengan lindo día!

With the new system, Nora should be able to:

- Create a menu for a specific date.
- Send a Slack reminder with today's menu to all chilean employees (this process needs to be asynchronous).

The employees should be able to:

- Choose their preferred meal (until 11 AM CLT).
- Specify customizations (e.g. no tomatoes in the salad).

Nora should be the only user to be able to see what the Cornershop employees have requested, and to create and edit today's menu. The employees should be able to specify what they want for lunch but they shouldn't be able to see what others have requested. 

NOTE: The slack reminders must contain an URL to today's menu with the following pattern https://nora.cornershop.io/menu/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (an UUID), this page must not require authentication of any kind.

## Aspects to be evaluated

Since the system is very simple (yet powerful in terms of yumminess) we'll be evaluating, besides functionality, these aspects:

- Testing
- Documentation
- Software design
- Programming style
- Repository history
- Appropriate framework use

## Aspects to be ignored

- Visual design of the solution
- Deployment of the solution

## Restrictions

- The usage of Django's admin is forbidden.
