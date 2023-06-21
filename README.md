# Bank API

This API provides a RESTful interface for interacting with a simple bank account system.
Features

    - User registration and login
    - Depositing funds into accounts
    - Withdrawing funds from accounts
    - Transferring funds between accounts
    - Viewing all transactions

### Usage

To use the API, you will need to first register a user. Once you have registered, you can log in and start interacting with your account.

To deposit funds into your account, you will need to make a POST request to the `/deposit` endpoint. The request body should contain the following data:
```
{
"amount": 1000,
"user_id": 1
}
```

To withdraw funds from your account, you will need to make a POST request to the `/withdraw` endpoint. The request body should contain the following data:
```
{
"amount": 500,
"user_id": 2
}
```

To transfer funds to another account, you will need to make a POST request to the `/transfer` endpoint. The request body should contain the following data:

```{
"recipient_id": 12345,
"amount": 100,
"user_id": 345
}
```