# Users

> Default posts request are newest posts, limited by 100 posts per-page requests.

### 1. Read Method

##### a. Users List

```bash
curl -X GET \
    -H 'Authorization: Token {header_token_key}' \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/users
```

**Example _(Users List)_:**

```bash
curl -X GET \
    -H 'Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9' \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/users
```

**Success Response:**

```json
[
  {
    "user": "agusmakmun",
    "last_login": "2018-03-02 03:01:02.019488+00:00",
    "date_joined": "2018-01-05 01:53:03+00:00",
    "total_posts": 10,
    "total_favorites": 3,
    "total_featured_posts": 1,
    "display_name": "Agus Makmun",
    "location": "Solo, Indonesia",
    "about_me": "Freelance developer. Currently doing more in backend, especially on Python and Django.",
    "website": "https://python.web.id",
    "twitter": "",
    "linkedin": "",
    "github": "https://github.com/agusmakmun",
    "birth_date": "2018-01-05"
  },
  {
    "user": "wallkathleen",
    "last_login": "2018-02-28 10:28:05.744120+00:00",
    "date_joined": "2018-02-26 06:13:50.234039+00:00",
    "total_posts": 2,
    "total_favorites": 2,
    "total_featured_posts": 1,
    "display_name": null,
    "location": null,
    "about_me": null,
    "website": null,
    "twitter": null,
    "linkedin": null,
    "github": null,
    "birth_date": null
  },
  {
    "user": "thomas",
    "last_login": null,
    "date_joined": "2018-02-26 06:07:25+00:00",
    "total_posts": 0,
    "total_favorites": 2,
    "total_featured_posts": 0,
    "display_name": null,
    "location": null,
    "about_me": null,
    "website": null,
    "twitter": null,
    "linkedin": null,
    "github": null,
    "birth_date": null
  }
]
```

##### b. Users Detail


```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/users/detail/{username}
```

**Example:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/users/detail/agusmakmun
```

**Success Response:**

```json
{
  "user": "agusmakmun",
  "last_login": "2018-03-02 03:01:02.019488+00:00",
  "date_joined": "2018-01-05 01:53:03+00:00",
  "total_posts": 10,
  "total_favorites": 3,
  "total_featured_posts": 1,
  "display_name": "Agus Makmun",
  "location": "Solo, Indonesia",
  "about_me": "Freelance developer. Currently doing more in backend, especially on Python and Django.",
  "website": "https://python.web.id",
  "twitter": "",
  "linkedin": "",
  "github": "https://github.com/agusmakmun",
  "birth_date": "2018-01-05"
}
```

-------------------------

### 2. Update Method

> All fields is non required fields. So, you can include one or more fields.

```bash
curl -X PUT \
    -H "Authorization: Token {header_token_key}" \
    -d "display_name={display_name}&location={location}&
        about_me={about_me}&website={website}&twitter={twitter}&
        linkedin={linkedin}&github={github}&birth_date={birth_date}" \
    https://python.web.id/api/v1/users/detail/{username}
```

**Example:**

```bash
curl -X PUT \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -d "display_name=Agus Changed&location=Palembang, Indonesia&
        about_me=This About me&website=https://python.web.id" \
    https://python.web.id/api/v1/users/detail/agusmakmun
```

**Success Response:**

```json
{
  "user": "agusmakmun",
  "last_login": "2018-03-02 03:01:02.019488+00:00",
  "date_joined": "2018-01-05 01:53:03+00:00",
  "total_posts": 10,
  "total_favorites": 3,
  "total_featured_posts": 1,
  "display_name": "Agus Changed",
  "location": "Palembang, Indonesia",
  "about_me": "This About me",
  "website": "https://python.web.id",
  "twitter": "",
  "linkedin": "",
  "github": "https://github.com/agusmakmun",
  "birth_date": "2018-01-05"
}
```

**Error Response:**

```json
{"detail":"You are not owner of this profile!"}
```
