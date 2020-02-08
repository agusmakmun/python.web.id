# Introduction

**Python Learning** helps to track posts, tags, and users metadata from new updates for web applications.
It is designed as a REST service. Please [register first](/accounts/signup/) to get new API.


### Per-Site Methods

> Each of these methods operates on a single site at a time, identified by the site parameter.

| Url                                                                     | Description                                     | auth required | methods           |
| ----------------------------------------------------------------------- | ----------------------------------------------- | :-----------: | :---------------: |
| [api/v1/login](/api/v1/docs/authentication/#1.-login)                   | To get a token authentication                   | no            | POST              |
| [api/v1/logout](/api/v1/docs/authentication/#2.-logout)                 | To logout from token request                    | yes           | GET               |
| [api/v1/auth](/api/v1/docs/authentication/#3.-check-authentication)     | To check API authentication                     | yes           | GET               |
|                                                                         |                                                 |               |                   |
| [api/v1/posts](/api/v1/docs/posts/#posts)                               | To get the posts _(with filter or no)_          | yes           | GET, POST         |
| [api/v1/posts/tagged/{slug}](/api/v1/docs/posts/#posts)                 | To get the posts contains with specific tag     | yes           | GET               |
| [api/v1/posts/author/{username}](/api/v1/docs/posts/#posts)             | To get the posts contains with specific author  | yes           | GET               |
| [api/v1/posts/detail/{slug}](/api/v1/docs/posts/#c.-detail-post)        | To get the detail post                          | yes           | GET, PUT, DELETE  |
|                                                                         |                                                 |               |                   |
| [api/v1/tags](/api/v1/docs/tags/#tags)                                  | To get the tags                                 | yes           | GET, POST         |
| [api/v1/tags/detail/{slug}](/api/v1/docs/tags/#c.-detail-tag)           | To get the detail tag                           | yes           | GET               |
|                                                                         |                                                 |               |                   |
| [api/v1/users](/api/v1/docs/users/#users)                               | To get the users                                | yes           | GET               |
| [api/v1/users/detail/{username}](/api/v1/docs/users/#b.-users-detail)   | To get the detail user                          | yes           | GET, PUT          |
