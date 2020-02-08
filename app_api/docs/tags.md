# Tags

> Default tags request are newest tags, limited by 500 per-page requests.

### 1. Read Method

##### a. Tags List

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags
```

**Example _(Tags List)_:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags
```

> We also providing a dynamic tags filter.

- param `q` is query input string to search something.
- param `page` is pagination number per-posts request.

##### b. Tags List Filter

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags?q={query}&page={numb}
```

**Example _(Tags List Filter)_:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags?q=django&page=1
```

**Success Response**


```json
[
  {
    "title": "Django Rest Framework",
    "slug": "django-rest-framework",
    "total_posts": 12
  },
  {
    "title": "Javascript",
    "slug": "javascript",
    "total_posts": 13
  },
  {
    "title": "Docker",
    "slug": "docker",
    "total_posts": 25
  },
  {
    "title": "Django",
    "slug": "django",
    "total_posts": 28
  },
  {
    "title": "Python",
    "slug": "python",
    "total_posts": 27
  }
  ....
]
```

##### c. Detail Tag

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags/detail/{slug}
```

**Example:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/tags/detail/django-rest-framework
```

**Success Response**

```json
{
  "title": "Django Rest Framework",
  "slug": "django-rest-framework",
  "total_posts": 12
}
```

-----------------------

### 2. Create Method

```bash
curl -X POST \
    -H "Authorization: Token {header_token_key}" \
    -d "title={title}&slug={slug}" \
    https://python.web.id/api/v1/tags
```

**Example:**

```bash
curl -X POST \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -d "title=Django Rest Framework&slug=django-rest-framework" \
    https://python.web.id/api/v1/tags
```
