# API Documentation

This document describes our REST API.

The API uses JSON format for requests and responses.

## Authentication

You need an API key to use our service.

The API key should be included in the header.

### Bearer Token

Include your API key in the Authorization header.

Use the format: `Authorization: Bearer YOUR_API_KEY`

### API Key Management

You can generate API keys from your dashboard.

Keys can be revoked at any time.

Each key has a unique identifier.

## Authentication

Our API supports Bearer token authentication.

You need an API key to use our service.

### Token Format

To authenticate, include your API key in the Authorization header.

The format is: `Authorization: Bearer YOUR_API_KEY`

All requests must include valid credentials.

### Managing Keys

API keys can be created and deleted from the dashboard.

You can have multiple active keys.

Keys should be kept secure and not shared.

## Endpoints

Our API provides several REST endpoints.

### User Management

#### GET /users

This endpoint retrieves all users.

Returns a list of users in JSON format.

The response includes user ID, name, and email.

#### GET /users

Retrieves the list of all users from the database.

The endpoint returns user information including ID, name, and email address.

Requires authentication to access.

#### POST /users

Creates a new user in the system.

You must provide name and email in the request body.

Required fields: name, email

Returns the created user object with an assigned ID.

#### Creating Users

To create a new user, send a POST request to /users endpoint.

Include name and email in the JSON request body.

The API will return the newly created user with an ID.

### Product Management

#### GET /products

Fetches all products from the catalog.

Returns product ID, name, price, and stock.

#### POST /products

Creates a new product.

Requires name, price, and description.

## Rate Limiting

Our API has rate limits to prevent abuse.

### Request Limits

Users are limited to 100 requests per hour.

The limit is 100 requests per hour per API key.

### Handling Rate Limits

If you exceed the limit, you'll receive a 429 error.

When you hit the rate limit, the API returns a 429 Too Many Requests error.

Wait before retrying your request.

## Error Handling

The API returns standard HTTP status codes.

### Status Codes

200 means success.

400 means bad request.

401 means unauthorized.

404 means not found.

429 means rate limit exceeded.

### Error Response Format

Errors include a JSON response with error details.

Error responses contain a message field describing what went wrong.

The response also includes an error code.

## Support

For help, contact support@example.com

### Contact Methods

If you need assistance, email us at support@example.com

Our support team is available 24/7.

### Support

Need help? Reach out to support@example.com

We respond within 24 hours.
