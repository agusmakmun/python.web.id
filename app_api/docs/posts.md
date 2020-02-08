# Posts

> Default posts request are newest posts, limited by 100 posts per-page requests.

### 1. Read Method

##### a. Posts List

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/posts
```

**Example _(Posts List)_:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    https://python.web.id/api/v1/posts
```

> We also providing a dynamic posts filter.

- param `q` is query input string to search something.
- param `sort` is specific order for the posts, default sort is `newest`.
- param `page` is pagination number per-posts request.

##### b. Posts List Filter

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    -d "q={query}&sort={newest,featured,views,votes,active}&page={numb}" \
    https://python.web.id/api/v1/posts
```

**Example _(Posts List Filter)_:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -d "q=django&sort=views&page=1" \
    https://python.web.id/api/v1/posts
```

**Success Response**

```json
[
  {
    "author": "iparker",
    "title": "Accept outside lose agent",
    "slug": "accept-outside-lose-agent",
    "description": "Build recognize against bar important..",
    "created": "2018-03-02T22:59:19.205421+07:00",
    "modified": "2018-03-04T10:15:57.809065+07:00",
    "publish": true,
    "tags": [
      "mysql",
      "html",
      "Django Rest Framework"
    ],
    "keywords": "mysql, django, rest api",
    "meta_description": "Accept outside lose agent.",
    "is_featured": false,
    "rating_likes": 1,
    "rating_dislikes": 2,
    "total_visitors": 388,
    "total_favorites": 4
  },
  {
    "author": "christopher34",
    "title": "Financial according else down week",
    "slug": "financial-according-else-down-week",
    "description": "Good here study citizen. Knowledge collection first continue.",
    "created": "2018-03-02T22:59:18.824240+07:00",
    "modified": "2018-03-02T22:59:19.075808+07:00",
    "publish": true,
    "tags": [
      "csv",
      "Docker",
      "Django",
      "Python"
    ],
    "keywords": "Stuff they ago until.",
    "meta_description": "Thing street result summer",
    "is_featured": false,
    "rating_likes": 5,
    "rating_dislikes": 0,
    "total_visitors": 453,
    "total_favorites": 3
  },
  ....
]
```

##### c. Detail Post

```bash
curl -X GET \
    -H "Authorization: Token {header_token_key}" \
    https://python.web.id/api/v1/posts/detail/{slug}
```

**Example _(Detail Post)_:**

```bash
curl -X GET \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    https://python.web.id/api/v1/posts/detail/completely-integrate-cooperative-total-linkage
```

**Success Response**

```json
{
  "author":"fulan",
  "title":"Completely integrate cooperative total linkage",
  "slug":"completely-integrate-cooperative-total-linkage",
  "description":"Continually administrate integrated models whereas interdependent human capital.",
  "created":"2018-01-05T14:12:15.258987+07:00",
  "modified":"2018-01-05T17:20:15.999470+07:00",
  "publish":true,
  "is_featured":false,
  "tags":[
    "Python",
    "Django"
  ],
  "keywords":null,
  "meta_description":"",
  "rating_likes":0,
  "rating_dislikes":0,
  "total_visitors":5,
  "total_favorites":2
}
```

-----------------------

### 2. Create Method

- The `keywords` and `meta_description` is not required field.

```bash
curl -X POST \
    -H "Authorization: Token {header_token_key}" \
    -d "title={title}&description={description}&tags={tags}&
        keywords={keywords}&meta_description={meta_description}&publish={publish}" \
    https://python.web.id/api/v1/posts
```

**Example:**

```bash
curl -X POST \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -d "title=This is post title&description=This Markdown Syntax&
        tags=Django, Javscript&keywords=hello, world&publish=true" \
    https://python.web.id/api/v1/posts
```

**Success Response**

```json
{
  "author":"fulan",
  "title":"This is post title",
  "slug":"this-is-post-title",
  "description":"This Markdown Syntax",
  "created":"2018-03-04T16:19:36.894998+07:00",
  "modified":"2018-03-04T16:19:36.895082+07:00",
  "publish":true,
  "is_featured":false,
  "tags":[
    "Javscript",
    "Django"
  ],
  "keywords":"hello, world",
  "meta_description":null,
  "rating_likes":0,
  "rating_dislikes":0,
  "total_visitors":0,
  "total_favorites":0
}
```

-----------------------

### 2. Update Method

```bash
curl -X PUT \
    -H "Authorization: Token {header_token_key}" \
    -d "title={title}&slug={slug}&description={description}&tags={tags}&
        keywords={keywords}&meta_description={meta_description}&publish={publish}" \
    https://python.web.id/api/v1/posts/detail/{slug}
```

**Example:**

```bash
curl -X PUT \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    -d "title=Change the title&description=Lorem Ipsum dolor ismet&tags=Django, Javascript&
        keywords=lay, me and do&publish=true" \
    https://python.web.id/api/v1/posts/detail/this-is-post-title
```

**Success Response**

```json
{
  "author":"fulan",
  "title":"Change the title",
  "slug":"change-the-title",
  "description":"Lorem Ipsum dolor ismet",
  "created":"2018-03-04T17:19:36.894998+07:00",
  "modified":"2018-03-04T17:19:36.895082+07:00",
  "publish":true,
  "is_featured":false,
  "tags":[
    "Javscript",
    "Django"
  ],
  "keywords":"lay, me and do",
  "meta_description":null,
  "rating_likes":0,
  "rating_dislikes":0,
  "total_visitors":0,
  "total_favorites":0
}
```

-----------------------

### 2. Delete Method

```bash
curl -X DELETE \
    -H "Authorization: Token {header_token_key}" \
    https://python.web.id/api/v1/posts/detail/{slug}
```

**Example:**

```bash
curl -X DELETE \
    -H "Authorization: Token f921c3a2fe4898d35985506c553e266113d6d4d9" \
    https://python.web.id/api/v1/posts/detail/this-is-post-title
```
