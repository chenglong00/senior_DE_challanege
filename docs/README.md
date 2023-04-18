# Design 1: Data Governance 

## Data Access Requirements (RBAC)
Logistics:
- Get the sales details (in particular the weight of the total items bought)
- Update the table for completed transactions
  - GRANT UPDATE TO transaction

Analytics:
- Perform analysis on the sales and membership status
- Should not be able to perform updates on any tables
  - GRANT READ to membership and transaction

Sales:
- Update database with new items
- Remove old items from database
  - GRANT write to items
  - GRANT delete to items

## Security
- use strong password for different database users
- restrict access to the database from outside the company's network using firewall
- enable SSL encryption to protect data in transit
- set up backup and recovery strategy 
  - regular backup the database and configuration settings
  - regular testing of recovery process
  - monitor the database for performance issues
  - set up alerts to notify us of any issues

## Design 2: System architecture for image processing pipeline
1. Users can upload