# House of Glamour API

## Project Description
This project is an e-commerce API built using Python and Flask. It provides functionalities for managing products, users, orders, and payments in an e-commerce platform.

## Features
- User authentication and authorization
- Product management (CRUD operations)
- Order management
- Payment processing

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/einbulinda/hseofgla-api.git
   cd hseofgla-api

2. Create abd activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`

3. Install dependencies
    pip install -r requirements.txt

4. Set up the environment variables (in a `.env` file):
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=your_database_url
    SECRET_KEY=your_secret_key

5. Run the application:
    flask run

## Usage
### Endpoints:
    * __GET__ /products: Retrieve all products
    * __POST__ /products: Add a new product
    * __GET__ /products/{id}: Retrieve a single product
    * __PUT__ /products/{id}: Update a product
    * __DELETE__ /products/{id}: Delete a product
    * __POST__ /users/signup: Sign up a new user
    * __POST__ /users/login: Log in an existing user


## Technologies Used
    * Python
    * Flask
    * SQLAlchemy
    * PostgreSQL

## Contributors
    * Einstein Bulinda (https://github.com/einbulinda)

## License
    This project is licensed under the MIT License - ee the LICENSE file for details.