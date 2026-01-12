# SEO Base Model (Best Practice)

This project includes a reusable **SEO Base Model** designed to solve real-world SEO and content lifecycle problems in Django applications.  
It is intentionally minimal, opinionated, and production-focused.

This is not a “nice to have” abstraction — it exists to prevent SEO-related technical debt.

---

## Why this base model exists

As soon as a Django project has more than one content model (pages, posts, categories, products, etc.), the same problems appear repeatedly:

- Every model needs SEO metadata
- Timestamps are redefined inconsistently
- Sitemap and caching logic lacks a reliable source of truth
- SEO changes require touching multiple models later

Without a shared base model:
- Fields get duplicated
- SEO behavior becomes unpredictable
- Future migrations become expensive and risky

This base model centralizes those concerns **once**, then enforces consistency everywhere.

---

## What the SEO Base Model provides

### 1. `meta_title` — Explicit control over the `<title>` tag

```python
meta_title = models.CharField(
    max_length=70,
    blank=True,
    help_text="Recommended: 50–60 characters"
)
```
## meta_title — Explicit SERP title control

```python
meta_title = models.CharField(
    max_length=70,
    blank=True,
    help_text="Recommended: 50–60 characters"
)
```

## Created_at — Content lifecycle tracking
```python
created_at = models.DateTimeField(auto_now_add=True)
```
## created_at — Content lifecycle tracking

**Why it exists**
- Records when content is first published into the system
- Enables:
  - Editorial workflows
  - Analytics and audits
  - Schema.org `datePublished`

**SEO note**
- Google does not rank pages based on creation date alone
- Transparent publishing data supports structured SEO

---

## updated_at — Freshness and reindexing signal

```python
updated_at = models.DateTimeField(auto_now=True)
```
## updated_at — Freshness and reindexing signal

**Why it exists**
- Essential for:
  - XML sitemaps
  - `Last-Modified` HTTP headers
  - Cache invalidation strategies
- Allows search engines to detect meaningful content updates

**SEO note**
- Freshness signals matter for time-sensitive and competitive queries
- This field enables those signals cleanly and consistently

---

## Why the model is abstract

```python
class Meta:
    abstract = True
```
This model does not create its own database table.

### Design intent
- Zero database overhead
- Fields are inherited by concrete models
- No unused or orphaned tables

This keeps the schema clean while enforcing shared SEO structure.

---

## Recommended usage

```python
class BlogPost(SeoBaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
```
By inheriting from this base model, every SEO-relevant object automatically includes:
- Metadata fields for search engines
- Reliable timestamps for freshness and indexing
- A consistent foundation for future SEO features

---

## Why this should exist from day one

SEO is **structural**, not cosmetic.

Adding this base model early:
- Prevents repeated migrations
- Avoids SEO-related refactors later
- Keeps optimization logic centralized and predictable

This model intentionally includes only what search engines and production systems actually need — nothing more, nothing less.


### `fallback: str` — What it means and why it exists

`fallback: str` is a **type hint**, not a Django or Python requirement.

---

### Usage in Template 

```html
<title>{{ object.get_meta_title(object.title) }}</title>
<meta name="description"  content="{{ object.get_meta_description }}">
<meta  name="description"
  content="{{ object.get_meta_description|default:object.content|tuncatechars:155 }}" >

```

or 
```python
def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)

    context = {
        "post": post,
        "seo_title": post.get_meta_title(post.title),
        "seo_description": post.get_meta_description(
            post.content[:155]
        ),
    }

    return render(request, "blog/detail.html", context)
```

then 
```html
<title>{{ seo_title }}</title>
<meta name="description" content="{{ seo_description }}">
```