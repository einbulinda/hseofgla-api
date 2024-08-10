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
    ```bash
    pip install -r requirements.txt

4. Set up the environment variables (in a `.env` file):
    ```bash
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=your_database_url
    SECRET_KEY=your_secret_key

5. Run the application:
    ```bash
    flask run

## Usage
### Endpoints:
    * GET /products: Retrieve all products
    * POST /products: Add a new product
    * GET /products/{id}: Retrieve a single product
    * PUT /products/{id}: Update a product
    * DELETE /products/{id}: Delete a product
    * POST /users/signup: Sign up a new user
    * POST /users/login: Log in an existing user


## Technologies Used
    * Python
    * Flask
    * SQLAlchemy
    * PostgreSQL

## Contributors
    * Einstein Bulinda (https://github.com/einbulinda)

## License
    This project is licensed under the MIT License - ee the LICENSE file for details.