# Tekana-eWallet - Technical evaluation at RSSB

<strong>Table of contents:</strong> <br>
1. [Strategy](#potential-strategy-to-rebuild-the-back-end-legacy-solution)
2. [Demo application](#demo-application)
    * [System requirements](#system-requirements)
    * [Tech stack](#tech-stack)
    * [Running the application](#running-the-application)
    * [API specification](#api-specification)
        * [Register User](#register-user)
        * [Get access token for authorization](#get-access-token-for-authorization)
        * [View a list of registered users](#view-a-list-of-registered-users)
        * [Account Funds Transfer](#account-funds-transfer)
        * [List Account Transactions](#list-account-transactions)


## Potential strategy to rebuild the back-end legacy solution
1. Gather requirements and understand the current system:
* Meet with the business team and product owner to gather a detailed understanding of the current system and its functionality
* Document the current system's architecture and technical stack
* Identify any pain points or challenges with the current system that need to be addressed in the new solution
2. Design the new back-end architecture:
 * Based on the requirements and current system, design a new back-end architecture that will meet the needs of the business and customers
 * Consider factors such as scalability, availability, fault-tolerance, security, and performance in the design
 * To improve performance, consider using the following:
    * Scalability: The system should be designed to scale horizontally, meaning that it can handle an increase in users by adding more resources (e.g. servers) rather than relying on a single, powerful server. This allows the system to handle a larger number of users without becoming overloaded
    * Caching: Caching can help reduce the load on the system by storing frequently accessed data in a temporary storage location, such as memory or disk. This allows the system to serve data to users more quickly, without having to retrieve it from a slower storage location (e.g. a database) each time it is requested
    * Load balancing: To ensure that the system can handle a large number of concurrent users, it would be necessary to use load balancing techniques to distribute incoming requests across multiple servers. This can help prevent any single server from becoming overloaded
    * Asynchronous processing: To further reduce the load on the system, one can consider using asynchronous processing techniques to allow the system to handle multiple requests at the same time without blocking. This can help improve the system's overall performance and reduce the response time for users
    * Database replicas: To avoid the database becoming a bottleneck, database replicas can help distribute the load across multiple database servers
 * Engage with the front-end team to ensure that the back-end architecture aligns with their needs and requirements
3. Develop the new back-end solution:
 * Using the chosen technology stack, begin developing the new back-end solution
 * Follow agile development methodologies, such as Scrum, to ensure that the project stays on track and meets the needs of the business
 * Engage with the front-end team regularly to ensure that the back-end solution aligns with their needs and requirements
4. Test and debug the new back-end solution:
 * Thoroughly test the new back-end solution to ensure that it is reliable and meets all requirements
 * Debug any issues that are found during testing
5. Deploy the new back-end solution:
 * Once the new back-end solution has been thoroughly tested and debugged, begin the process of deploying it to the production environment.
 * Follow best practices for deploying a new solution to ensure a smooth transition such as the following:
    * Create a deployment schedule
    * Create a rollback plan in case the deployment encounters any issues
    * Train relevant users on the new solution and how to use it
    * Communicate the deployment to all relevant parties, including employees and customers
    * Perform the deployment during a time when it will have minimal impact on users, such as during non-peak hours
    * Provide support to users during the transition period to ensure a smooth transition
6. Monitor and maintain the new back-end solution:
 * Once the new back-end solution is live, monitor it closely to ensure that it is performing as expected
 * Address any issues or bugs that are discovered post-launch
 * Regularly perform maintenance and updates to keep the solution up-to-date and secure

 ## Demo application

 ### System requirements:
 1. Installed Python 3.8 or above
 2. 2 CPUs or more
 4. 4 GB RAM or more

 Note: The app was tested on a linux system (Ubuntu 20.04)

 ### Tech stack:
 1. Django
 2. Django Restframework
 3. SQLite DB (For demo purpose and easy of testing)

 ### Running the application:
On terminal (CMD) where python is configured in PATH, run the following commands in order:
1. Change to the directory containing source code: 
```
cd /path/to/path/Tekana-eWallet
```
2. Create a virtual environment to isolate project dependencies
```
python -m venv .venv
```
3. Activate the environment
```
source .venv/bin/activate
```
4. Install dependency packages
```
pip install -r requirements.txt
```
5. Create the SQLlite DB and apply model migrations
```
python manage.py migrate
```
6 Run the server (uses the development server for the purpose of testing)
```
python manage.py runserver
```

After everything is successful, the server is reachable at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### API specification
The following serves an API documentation. Remember to set the `Content-Type` header with `application/json` value

#### <strong>Register User</strong>
---
URI: `/api/register` <br>
Method: `POST` <br>

Request payload:
```json
{
    "email": "<user-email>",
    "password": "<password>",
    "first_name": "<first-name>",
    "last_name": "<last-name>"
}
```
Example response payload
```json
{
    "message": "User Created Successfully. Login to get authorization token",
    "data": {
        "accounts": [
            {
                "owner_user_uuid": "993f73ae-0581-4a51-ab88-2a9ad71c5753",
                "uuid": "1d3c2f29-fe7b-43b1-8979-f989b913a0aa",
                "created_at": "2023-01-06T14:10:09.511525Z",
                "is_deleted": false,
                "modified_at": "2023-01-06T14:10:09.511533Z",
                "balance": 0.0,
                "is_active": true,
                "account_type": null,
                "name": "Primary"
            }
        ],
        "last_login": null,
        "is_staff": false,
        "is_active": true,
        "date_joined": "2023-01-06T14:10:09.291809Z",
        "uuid": "993f73ae-0581-4a51-ab88-2a9ad71c5753",
        "created_at": "2023-01-06T14:10:09.291828Z",
        "is_deleted": false,
        "modified_at": "2023-01-06T14:10:09.291831Z",
        "email": "claude@gmail.com",
        "first_name": "Clude",
        "last_name": "Narambe",
        "verified": false,
        "groups": [],
        "user_permissions": []
    },
    "errors": null
}
```
#### <strong>Get access token for authorization</strong>
---
URI: `/api/token` <br>
Method: `GET` <br>

Request payload:
None

Example response payload
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MzEwMDkwNCwiaWF0IjoxNjczMDE0NTA0LCJqdGkiOiJjNTgzYjhjOGIzNjk0NDE5Yjk1NTRkMzczY2NjZjc4NSIsInVzZXJfaWQiOjR9.OGaPSa1WCXpcIZjThKG_vQ2tkt7b7tUrfynt4IcmnCM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczMDE0ODA0LCJpYXQiOjE2NzMwMTQ1MDQsImp0aSI6ImJhZDgwZWZmZGMxZDQzNTE5N2M2MDczNjU5OGFiZmY4IiwidXNlcl9pZCI6NH0.H1qpatQM6D8koOq5Nu_4w8VtNHPP75fjyMs14MtDfm8"
}
```

#### <strong>View a list of registered users</strong>
---
N.B: Requires to be authenticated. Set the following header `Authorization: "Bearer <access-token>"` <br>

URI: `/api/users` <br>
Method: `GET` <br>

Request payload: None

Example response payload
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "accounts": [
                {
                    "owner_user_uuid": "702927aa-be8b-4610-a306-431e7c14c17c",
                    "uuid": "80b65af0-2533-444f-9bf1-52bd78fe2ff9",
                    "created_at": "2023-01-03T13:09:50.052695Z",
                    "is_deleted": false,
                    "modified_at": "2023-01-03T13:09:50.052709Z",
                    "balance": 979.1000000000001,
                    "is_active": true,
                    "account_type": null,
                    "name": "Primary"
                }
            ],
            "last_login": null,
            "is_staff": false,
            "is_active": true,
            "date_joined": "2023-01-03T13:09:49.752633Z",
            "uuid": "702927aa-be8b-4610-a306-431e7c14c17c",
            "created_at": "2023-01-03T13:09:49.752655Z",
            "is_deleted": false,
            "modified_at": "2023-01-03T13:09:49.752660Z",
            "email": "john-b@gmail.com",
            "first_name": "John",
            "last_name": "Black",
            "verified": false,
            "groups": [],
            "user_permissions": []
        },
        ...
    ]
}
```

#### <strong>Account Funds Transfer</strong>
---
N.B: Requires to be authenticated. Set the following header `Authorization: "Bearer <access-token>"` <br>

URI: `/api/accounts/transfer` <br>
Method: `GET` <br>

Request payload:
```json
{
    "sender_account_uuid": "<account-uuid>",
    "receiver_account_uuid": "<account-uuid>",
    "amount": <amount-to-transfer>,
    "reason": "<reason>",
    "notes": ""
}
```

Request payload's fields description:
* <i>sender_account_uuid</i> (str, required) - uuid field of an account object. Represents an account from which the money will deducted
* <i>receiver_account_uuid</i> (str, required)  - uuid field of an account object. Represents an account to which the money will be added
* <i>amount</i> (str, required) - The amount to deduct. Cannot be more than the sender acount's balance or less than 0
* <i>reason</i> (str, optional)
* <i>notes</i> (str, optional)


Example response payload <br>

N.B: <i>Returns 2 transactions, one debiting sender account and another crediting receiver account </i>

```json
{
    "message": "The transfer transaction was successful!",
    "data": [
        {
            "sender_account_uuid": "80b65af0-2533-444f-9bf1-52bd78fe2ff9",
            "receiver_account_uuid": "b7cbc6a6-0d70-4b1d-b610-7e2897dabb3d",
            "uuid": "6017ca02-6e4d-4893-811b-4a0b4e7c6c6f",
            "created_at": "2023-01-06T14:34:23.469190Z",
            "is_deleted": false,
            "modified_at": "2023-01-06T14:34:23.469196Z",
            "amount": 25.0,
            "status": "Complete",
            "reason": "Reimbursement",
            "notes": "",
            "transaction_type": "Debit",
            "account_balance_before": 979.1000000000001,
            "account_balance_after": 954.1000000000001
        },
        {
            "sender_account_uuid": "80b65af0-2533-444f-9bf1-52bd78fe2ff9",
            "receiver_account_uuid": "b7cbc6a6-0d70-4b1d-b610-7e2897dabb3d",
            "uuid": "5ee3ca8d-5996-4ded-8e16-a8d8fc6b484e",
            "created_at": "2023-01-06T14:34:23.469231Z",
            "is_deleted": false,
            "modified_at": "2023-01-06T14:34:23.469234Z",
            "amount": 25.0,
            "status": "Complete",
            "reason": "Reimbursement",
            "notes": "",
            "transaction_type": "Credit",
            "account_balance_before": 20.900000000000006,
            "account_balance_after": 45.900000000000006
        }
    ],
    "errors": null
}
```

#### <strong>List Account Transactions</strong>
---
N.B: Requires to be authenticated. Set the following header `Authorization: "Bearer <access-token>"` <br>

URI: `/api/accounts/<account-uuid>/transactions` <br>
Method: `GET` <br>

Request payload: `None`

Example response payload
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "sender_account_uuid": "80b65af0-2533-444f-9bf1-52bd78fe2ff9",
            "receiver_account_uuid": "b7cbc6a6-0d70-4b1d-b610-7e2897dabb3d",
            "uuid": "5ee3ca8d-5996-4ded-8e16-a8d8fc6b484e",
            "created_at": "2023-01-06T14:34:23.469231Z",
            "is_deleted": false,
            "modified_at": "2023-01-06T14:34:23.469234Z",
            "amount": 25.0,
            "status": "Complete",
            "reason": "Reimbursement",
            "notes": "",
            "transaction_type": "Credit",
            "account_balance_before": 20.900000000000006,
            "account_balance_after": 45.900000000000006
        },
        {
            "sender_account_uuid": "b7cbc6a6-0d70-4b1d-b610-7e2897dabb3d",
            "receiver_account_uuid": "80b65af0-2533-444f-9bf1-52bd78fe2ff9",
            "uuid": "25653c29-b39a-4cc3-9725-284acd034577",
            "created_at": "2023-01-03T14:54:58.931598Z",
            "is_deleted": false,
            "modified_at": "2023-01-03T14:54:58.931636Z",
            "amount": 25.0,
            "status": "Complete",
            "reason": "Payment",
            "notes": "",
            "transaction_type": "Debit",
            "account_balance_before": 45.900000000000006,
            "account_balance_after": 20.900000000000006
        },
        ...
    ]
}
```

