# Shopify Backend Developer Intern Challenge - Summer 2022
# Shopify Production Engineering Intern Challenge - Summer 2022

## Installation and Setup

1. Install Python 3.x in your environment
2. Install all dependent packages using : pip install -r ShopifyInternshipApplication\shopify\resource\install\requirements.txt
3. Configure a MySQL DB and update it's details in ShopifyInternshipApplication\shopify\resource\config\settings_prod.yaml
4. Using the SQL commands in ShopifyInternshipApplication\shopify\db\sql\table.sql setup the database and tables within MySQL server
5. Update the configurations for your environment within ShopifyInternshipApplication\shopify\resource\config\settings_prod.yaml
6. Set environment variable APP_ENV to 'prod', this tells the python server program to look for configurations in settings_prod.yaml
7. You can run server using this command python ShopifyInternshipApplication\shopify\service\main\app.py
8. Now your server is running on the port as defined in the settings

The server has been hosted on AWS.
Backend : http://35.164.86.119:9086/api/inventory/list
Frontend : http://35.164.86.119:9087/
