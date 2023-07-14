# GebeyaHub Online Store

Welcome to the GebeyaHub Online Store repository! This repository contains the source code for an e-commerce web application.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Motivation](#Motivation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GebeyaHUB is an innovative website created by Nathan Assefa Kassa and Mahlet Seifu Feleke to revolutionize shopping and trading in Ethiopia. We developed it as a portfolio project for Holberton School to showcase our web development skills.

---

The Online Store is a web application designed to provide a platform for users to browse and purchase products online. It offers a user-friendly interface that allows customers to search for products and add them to their cart.

## Features

- User authentication: Users can sign up, log in, and log out.
- Product browsing: Users can view a list of products, search for specific products, and view detailed information about each product.
- Shopping cart: Users can add products to their cart, modify the quantity, and remove items.

## Motivation

The GebeyaHUB project came from our desire to demonstrate our abilities and apply what we had learned in the past 10 months. We had several project ideas but decided to create an e-commerce website because it was relevant and had the potential to make a difference in the Ethiopian market. This project served as proof of our skills and a way to address the challenges faced by businesses and consumers in our country.

## Usage

### Prerequisites

- Python (version 3.6 or higher)
- Flask (version 2.0.1 or higher)
- SQLAlchemy (version 1.4.22 or higher)
- MySQL (version 5.7 or higher)

### Installation

1. Clone the repository:

    git clone https://github.com/nathan-assefa/Online_store.git

2. Navigate to the project directory:

    cd Online_store

3. Install the dependencies:

    pip install Flask==2.0.1
    pip install SQLAlchemy==1.4.22
    pip install mysqlclient==2.1.0

4. Create a MySQL database for the application.

5. Update the database connection configuration in the config.py file:
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database_name'
   
Replace username, password, and database_name with your own MySQL database credentials.

6. Start the application:

The application will be accessible at http://localhost:5000.

Once the application is up and running, you can access it in your web browser by navigating to http://localhost:5000. From there, you can create an account, browse products, and add them to your cart.

## Authors

| Team Name | LinkedIn Account                           | GitHub Account                          |
|-----------|--------------------------------------------|-----------------------------------------|
| Nathan Assefa    | [Nathan's LinkedIn](https://www.linkedin.com/in/nathan-assefa-9ba017253/)     | [Nathan's GitHub](https://github.com/nathan-assefa)     |
| Mahlet Seifu    | [Mahlet's LinkedIn](https://www.linkedin.com/in/mahlet-seifu-feleke) | [Mahlet's GitHub](https://github.com/Mahlet2123) |


## Contributing

Contributions to the Online Store project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

The Online Store project is licensed under the MIT License. Feel free to use and modify the code for your own purposes.
