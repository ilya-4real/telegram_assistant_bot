## Description
This is a telegram bot that helps with daily routine. It is deployed until 6th april on Render.com, go ahead and try it if it is still available. 

\
**Telegram username** : 

`@assist_weather_tasks_bot` 

## Features

Mainly it does 3 things: 
 - show current weather in your city
 - show exchange rates for currencies that you set
 - manage your tasks
 - notify when task expires (works badly because of free deployment)

 ## Available commands
`/getme` - get your profile settings \
`/dropstate` - exit from any process \
`/weather` - get current weather \
`/currency` - get current rates \
`/tasks` - manage your tasks \
`/add_task` - add new task  \
`/set_city` - set your city for weather \
`/add_currency` - add currency symbol for currency rates 

## Technologies used
`aiogram` - as an asynchronious Telegram API framework \
`sqlalchemy` - as SQL toolkit. paired with `asyncpg` as a driver \
`postgreSQL` - as SQL database \
`apscheduler` - for tracking tasks time 

## Improvement guide
Architecturally the application is built according to **onion structure**. It is divided in 4 parts:
 - **Application layer** - layer of framework specific implementation
 - **Service layer** - layer of business logic
 - **Repository layer** - layer for controlling domain models
 - **Domain** - Database models, that are main for the application.

 Main methods that could be needed for working with database are already implemented in `SQLalchemyRepitory` class. 

 \
To add a feature you should:
 - Implement a method that would be needed on **Repository** layer for controlling model.
 - Implement a main business logic on **Service layer**.
 - Implement a handler/callback for telegram.