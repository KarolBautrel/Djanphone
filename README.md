# Djanphone - ecommerce app
 Djanphone app created with Django and Bootstrap

## Table of content

  * [ General Info](#general-info) 
  * [Technologies](#technologies)
  * [Setup](#setup)
  * [App structure](#app-structure)
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
## App Structure
```

```
## Features
The main goal of this project is creating an online shop which will include all features that the real shop has. 
### Feateures list
* [Navbar](#Navbar)
* [Home](#Home)
* [Product List](#Product-list)
* [Product detail](#Product-detail)
* [Adding comments](#Adding-comments)
* [Buying products](#Buying-products)
* [Writing tickets](#Writing-tickets)
* [Moderator panel](#Moderator-panel)
* [User panel](#User-panel)
* [Contact](#Contact)

#### Navbar
Navbar includes
* Home - redirects to home view
* Products - redirects to Product list view
* Store - redirect to local stores view
* Contact - redirect to contact non-registered user view
* Login - for login
* Signup for signup
Also, when user is logged in the right sight of navbar is changing to 
* Dropdown menu included Progfile, Account Setting, ticket options, logout option and if user is moderator moderator panel.
* Cart which shows quantity of products inside. 
* Notification icon for message sent by staff.
<!-- TO DO PICTURES -->
#### Home
In home screen I've decided to put an little widget, which shows user's city actual temperature, weather, humidity and pressure. This widget is using with external
api called "weather-api". There is also a log in button which redirects to login view. 
<!-- TO DO PICTURES -->
#### Product List
Product list includes all available products to buy from shop, the pagination is set to 4, so we can see 4 products on one site. Also if some product
is bestseller we can see patch of it, and when product is on discount we can see non discount price so we know how much money we can save. 
If we click on <strong>DETAIL</strong> button, we are going to be redirected to product detail view
<!-- TO DO PICTURES -->
#### Product Detail
After click on <strong>DETAIL</strong> button in product List we are going to product detail view, which includes the full picture of product, his price, patch and description. In this view we have two buttons. <strong>Add to cart</strong> is adding the product to the cart and also redirects us to cart view and the second one <strong>Add review of product</strong> is allowing authenticated user to make a comment which is shown under the product detail.
<!-- TO DO PICTURES -->
#### Adding comments
After click on <strong>Add review of product</strong> if we are logged in we are able to write a review of product which is shown in detail product view. Also if we want to delete it we are able to do this but only to reviews we made. 
####Buying products
After click on <strong>Add to cart</strong> we are getting redirected to 


