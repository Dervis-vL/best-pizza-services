"""Response schemas for the pizza API."""

import pydantic as pyd


class ScrapeResultSchema(pyd.BaseModel):
    """Counts from a scraping pass."""

    model_config = pyd.ConfigDict(from_attributes=True)

    scraped: int
    failed: int


class ParseResultSchema(pyd.BaseModel):
    """Counts from a parsing pass."""

    model_config = pyd.ConfigDict(from_attributes=True)

    parsed: int
    skipped: int


class AddCategoryResponse(pyd.BaseModel):
    """Response body for a completed add-category cycle."""

    model_config = pyd.ConfigDict(from_attributes=True)

    editions_scraped: ScrapeResultSchema
    editions_parsed: ParseResultSchema
    webpages_scraped: ScrapeResultSchema
    webpages_parsed: ParseResultSchema
