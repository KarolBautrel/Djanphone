# Djanphone - ecommerce app
 Djanphone app created with Django and Bootstrap

## Table of content

  * [ General Info](#general-info) 
  * [Technologies](#technologies)
  * [Setup](#setup)
  * [Features](#features)

## General info
This project is imitation of phone online shop with full CRUD actions, including writing tickets, making checkouts and paypal payments.

## Technologies
Project is created with:
* Python version: 3.9
* Django version: 4.0
* MDBootsrtap version: 5.0
* HTML 

## Setup
To run setup first create virtual environment
```
python -m venv venv
```
Then, after your venv folder is created open it by 
```
venv\scripts\activate
```
And then install requirements included in filde requirements.txt
```
pip install -r requirements.txt
```
After instalation complete you can run server with project
```
python manage.py runserver
```
## Features
The main goal of this project is creating an online shop which will include all features that the real shop has. 
### Feateures list
* [Home](#Home)
* [Product List](#Product-list)
* [Product detail](#Product-detail)
* [Adding comments](#Adding-comments)
* [Buying products](#Buying-products)
* [Writing tickets](#Writing-tickets)
* [Moderator panel](#Moderator-panel)
* [User panel](#User-panel)
* [Contact](#Contact)

#### Home
In home screen I've decided to put an little widget, which shows user's city actual temperature, weather, humidity and pressure. This widget is using with external
api called "weather-api". There is also a log in button which redirects to login view. 
