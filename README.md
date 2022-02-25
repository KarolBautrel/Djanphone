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
* [Navbar](#Navbar)
* [Home](#Home)
* [Product List](#Product-list)
* [Product detail](#Product-detail)
* [Adding comments](#Adding-comments)
* [Buying products](#Buying-products)
* [Local stores](#Local-stores)
* [Writing tickets](#Writing-tickets)
* [Notifications](#Notifications)
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
#### Buying products
After click on <strong>Add to cart</strong> we are getting redirected to our cart, which includes every product we added to cart. If we added product twice, then its quantity will be set to 2 and etc. Also in cart we can managing products and quantity. If we click on <strong>+</strong> button we can add one more of product to cart, also if we click
<strong>-</strong> we are able to decrease it. If we reach 0, then product is automatically deleted from cart. Also we can delete whole product with his quantity with one button
<strong>DELETE PRODUCT</strong>. In cart we have also total price of products which includes coupon we can use, but about this later<!-- TO DO PICTURES OF CART WITH PRODUCT -->.
If we dont have any product we are getting redirect to homepage with flash message that we dont have any active orders. Also if we want to keep shopping we have button called
<strong> Continue shopping !</strong> which redirect us to product list view and also we can proceed to checkout with <strong>Get to the checkout</strong>button.
##### Payments
After proceeding to chekout we need to fulfill the shipping address. If we select option called <b>Billing address is the same as my shipping address</b> the billing address 
will be created automatically and we will be redirect strict to payment view. Also on right side of screen we have option of adding coupons. If we have one, and add it our 
total price will decrease of amount of coupon. Payment at this moment is set only for paypal.
### Local Stores
Djanphone also has 2 local stores which are place in Vaticano and in Poland, Zielona Gora. In view we can see google map which shows exactly where the shop is. Also we can get
into shop detail and see list of product available in local store. Also if user is shop moderator he can manage products and add/remove products which are not or which are arrived to local store.
#### Tickets
In navbar dropdown menu on right side we can see options <b> Ticket</b> and <b>Ticket panel</b>. The first is redirect us to ticket creation view, where we can write subject of ticket and description of problem. After createin in <b> Ticket panel </b> created ticket is visible, we can see subject, created date and also status of ticket which can be open or closed. After clicking on <b> Ticket details</b> we are able to see details of ticket which include all informations about it. 
#### Notifications(Messages)
The last object on navbar is notification icon. This tool is set if staff wants to notificates regular users about something. If notification is send then there will be red
exclamation on icon. If we click on it we are able to see our inbox which stores all messages from staff, we are able to see details of message and we can from there mark it as readed. And also we can delete message. If message will be mark as readed or deleted, then exclamation will vanish. 
#### Moderator Panel 
If user is moderator, in dropdown menu there will be option called "Admin Panel", from there he is able to send mass messages and creating new products, new products must be 
approved by superuser(admin) to prevent mistakes. 
#### User Panel
In user panel, regular user is able to make some crud options about his account like update informations but also he can reset password, change password, change email and link his account with social account ( right now with google account)
#### Contact
Contact view is declared for users without account or for users who doesnt want to be linked with account. After fullfill required fields, on email writed in view will be 
send email with confirmation that message is sent. 
