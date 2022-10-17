# Motivator_users

This is a web service designed for display results of requests to [Motivation API](https://github.com/Bahch1k/Motivator_motivations) with the ability to register a users.

## Created with

* Django 4.0.6 
* Redis 6.0
* PostgreSQL 14.3

## Features

* The necessary parts of the service are placed in Docker containers linked together in a `docker-compose` file.
* The service implemented caching of a page with the list of motivations using Redis as a backend.
* The sending motivations to the API is logged.
* It is possible to test requests to the API using the unittests which are available in the project (the `pytest` library is used).

### Attention

This service is an add-on that demonstrates the possibility of requests to the [API](https://github.com/Bahch1k/Motivator_motivations) and the correctness of its work. User registration and authorization functions are available without connecting to the [API](https://github.com/Bahch1k/Motivator_motivations). I recommend looking at the documentation for the [Motivation API](https://github.com/Bahch1k/Motivator_motivations) first.
