# Authentication

All requests to Python Learning API require you to authenticate yourself to the service. In order to do this you must login first to get a `token` for all requests.

### 1. Login

- param `username` is your username to login.
- param `password` is your password to login.

> If you using 3d party app for login authentication, you must [set a password](/accounts/password/set/) first.

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{'username':'username', 'password':'password'}" \
    https://python.web.id/api/v1/login
```

**Example:**

```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{'username':'fulan', 'password':'mypassword123'}" \
    https://python.web.id/api/v1/login
```

**Success Response:**

> This `token` uses for all requests to Python Learning API.

```json
{"token":"f921c3a2fe4898d35985506c553e266113d6d4d9"}
```

- param `token` is generated token after logged in.

**Error Response:**

```json
{"non_field_errors":["Unable to log in with provided credentials."]}
```

- param `non_field_errors` is error message if one or both of fields is incorrect.

------------------

### 2. Logout

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/logout
```

**Example:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/logout
```

**Success Response:**

```json
{"detail":"You are logout!"}
```

**Error Response:**

```json
{"detail":"You are not logged in!"}
```

------------------

### 3. Check Authentication

> To makesure the `token` is registered or activated, you can re-check the header token which following this commands.

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/auth
```

**Example:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/auth
```

**Success Response:**

```json
{"id":1,"token":"f921c3a2fe4898d35985506c553e266113d6d4d9","username":"fulan"}
```

- param `id` is user id/pk.
- param `token` is generated token after logged in.
- param `username` is username of user.

**Error Response:**

```json
{"detail":"Invalid token."}
```
