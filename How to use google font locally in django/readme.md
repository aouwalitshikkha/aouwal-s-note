# How to use Google Font Locally 

I originally loaded Inter from Google Fonts, but switched to self-hosting to remove third-party requests and keep font loading fully under my control. The Lighthouse gain is small, but the setup is simple and predictable.

## What I did

I downloaded Inter directly from the official GitHub releases
https://github.com/rsms/inter/releases
You can download directly from google fonts
From the archive, I only kept the web .woff2 files and ignored ttf, otf, and variable fonts.

## Static file Layout
```text
static/
├─ fonts/
│  └─ inter/
│     ├─ Inter-Regular.woff2
│     ├─ Inter-Medium.woff2
│     ├─ Inter-SemiBold.woff2
│     └─ Inter-Bold.woff2
└─ css/
   └─ fonts.css
```

I limited the weights to the ones actually used in the UI.

## Font definition
```css
@font-face {
  font-family: 'Inter';
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  src: url('../fonts/inter/Inter-Regular.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-weight: 500;
  font-style: normal;
  font-display: swap;
  src: url('../fonts/inter/Inter-Medium.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-weight: 600;
  font-style: normal;
  font-display: swap;
  src: url('../fonts/inter/Inter-SemiBold.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-weight: 700;
  font-style: normal;
  font-display: swap;
  src: url('../fonts/inter/Inter-Bold.woff2') format('woff2');
}

```
font-display: swap prevents invisible text during load and avoids Lighthouse warnings.

## Django template setup
In base.html, I removed all Google Fonts <link> tags and replaced them with:

```django
{% load static %}

<link rel="preload"
      href="{% static 'fonts/inter/Inter-Regular.woff2' %}"
      as="font"
      type="font/woff2"
      crossorigin>

<link rel="stylesheet" href="{% static 'css/fonts.css' %}">
```
Only the regular weight is preloaded to avoid over-preloading.

## Usage
```css
body {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```
### Result

- No requests to `fonts.googleapis.com` or `fonts.gstatic.com`
- Fonts load from `/static/fonts/`
- Slightly cleaner Lighthouse report
- One less external dependency

This setup keeps typography boring and reliable, which is exactly what I want.

