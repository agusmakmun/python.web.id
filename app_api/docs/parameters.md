# Parameters

#### Global

- `detail` _(String)_ - is an success or error message.


#### Authentication

- param `id` _(Int)_ - is user id/pk.
- param `token` _(String)_ - is generated token after logged in.
- param `username` _(String)_ - is username of user.
- param `password` _(String)_ - is password of user.


#### Posts

- param `author` _(String)_ - is username of author.
- param `title` _(String)_ - is title of post.
- param `slug` _(String Slug)_ - is slug url of post.
- param `description` _(String)_ - is description of post which following the markdown format.
- param `created` _(String Date)_ - is created time of post.
- param `modified` _(String Date)_ - is modified time of post.
- param `publish` _(Boolean)_ - is status of post.
- param `tags` _(Array)_ - is array of tag names.
- param `keywords` _(String)_ - is additional meta keywords for post _(split by comma)_.
- param `meta_description` _(String)_ - is additional meta description of post.
- param `is_featured` _(Boolean)_ - is another status of post is featured or not.
- param `rating_likes` _(Int)_ - is total rating likes contains with each post.
- param `rating_dislikes` _(Int)_ - is total rating dislikes contains with each post.
- param `total_visitors` _(Int)_ - is total visitors that has been visited on each post.
- param `total_favorites` _(Int)_ - is total favorites from another users.


#### Tags

- param `title` _(String)_ - is title of tag.
- param `slug` _(String Slug)_ - is slug url of tag.
- param `total_posts` _(Int)_ - is total of posts contains with each tag.


#### Users

- param `user` _(String)_ - is default username of user.
- param `last_login` _(String Date)_ - is default user last login session.
- param `date_joined` _(String Date)_ - is default user registered date.
- param `total_posts` _(Int)_ - is total user posts.
- param `total_favorites` _(Int)_ - is total user favorites.
- param `total_featured_posts` _(Int)_ - is total user featured posts.
- param `display_name` _(String)_ - is additional name of user to display.
- param `location` _(String)_ - is additional location of _(Recomended: City, Country)_.
- param `about_me` _(Log String)_ - is additional description about user.
- param `website` _(String Url)_ - is additional website url.
- param `twitter` _(String Url)_ - is additional twitter url.
- param `linkedin` _(String Url)_ - is additional linkedin url.
- param `github` _(String Url)_ - is additional github url.
- param `birth_date` _(String Date)_ - is additional birth date.
