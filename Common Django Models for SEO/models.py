from django.db import models


class SeoBaseModel(models.Model):
    """
    Base model for SEO and content freshness.

    This model is intended to be inherited by all SEO-relevant models
    (pages, posts, categories, products, etc.) to ensure consistent
    metadata and timestamp handling across the project.
    """

    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Recommended: 50–60 characters. Optional override for the HTML <title> tag."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Recommended: 140–160 characters. Used for search result snippets."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the object was first created (used for publishing data)."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp updated on every save (used for freshness, sitemaps, caching)."
    )

    class Meta:
        abstract = True
        ordering = ["-updated_at"]

    def get_meta_title(self, fallback: str | None = None) -> str:
        """
        Returns the meta title if provided, otherwise falls back
        to the supplied value (usually the object's main title).
        """
        return self.meta_title or fallback or ""

    def get_meta_description(self, fallback: str | None = None) -> str:
        """
        Returns the meta description if provided, otherwise falls back
        to the supplied value (usually derived from content).
        """
        return self.meta_description or fallback or ""
