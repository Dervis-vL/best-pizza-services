"""Category dependency providers."""

from typing import Annotated

from fastapi import Depends

from geolocation import GeolocationService
from geolocation.application import use_cases as geo_use_cases
from pizza_api.application import use_cases
from pizza_api.dependencies.repositories import (
    HtmlRepoDep,
    PizzeriaRepoDep,
    RankingRepoDep,
)
from pizza_data_collector import models as collector_models
from pizza_data_collector import parsers, scrapers
from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage.application import use_cases as storage_use_cases


def get_add_category_uc(
    ranking_repo: RankingRepoDep,
    pizzeria_repo: PizzeriaRepoDep,
    html_repo: HtmlRepoDep,
) -> use_cases.AddCategoryUseCase:
    """Build and wire the AddCategoryUseCase with all its dependencies."""
    scrape_uc = collector_use_cases.ScrapeUseCase(
        scraper=scrapers.Scraper(http_client=scrapers.HttpClient()),
    )
    parse_edition_uc = collector_use_cases.ParseEditionUseCase(
        parser=parsers.EditionParser(
            awards_patterns=collector_models.award_name_patterns,
            card_patterns=collector_models.card_patterns,
            url_pattern=collector_models.url_pattern,
            position_patterns=collector_models.ranking_position_patterns,
        ),
    )
    parse_pizzeria_uc = collector_use_cases.ParsePizzeriaUseCase(
        parser=parsers.PizzeriaParser(
            coord_patterns=collector_models.coordinate_patterns,
            address_patterns=collector_models.adress_patterns,
            phone_patterns=collector_models.phone_patterns,
        ),
    )
    enrich_geo_uc = geo_use_cases.EnrichGeolocationUseCase(
        geolocation_service=GeolocationService(user_agent="best-pizza-services/1.0"),
    )

    return use_cases.AddCategoryUseCase(
        seed_uc=storage_use_cases.SeedCategoriesAndEditionsUseCase(
            ranking_repository=ranking_repo,
        ),
        scrape_editions_uc=use_cases.ScrapeEditionsUseCase(
            get_editions_uc=storage_use_cases.GetEditionsUseCase(
                ranking_repository=ranking_repo,
            ),
            scrape_uc=scrape_uc,
            store_html_uc=storage_use_cases.StoreEditionHtmlUseCase(
                html_repository=html_repo,
            ),
            mark_scraped_uc=storage_use_cases.MarkEditionAsScrapedUseCase(
                ranking_repository=ranking_repo,
            ),
        ),
        parse_editions_uc=use_cases.ParseEditionsUseCase(
            get_editions_uc=storage_use_cases.GetEditionsUseCase(
                ranking_repository=ranking_repo,
            ),
            get_html_uc=storage_use_cases.GetEditionHtmlUseCase(
                html_repository=html_repo,
            ),
            parse_edition_uc=parse_edition_uc,
            mark_parsed_uc=storage_use_cases.MarkEditionAsParsedUseCase(
                ranking_repository=ranking_repo,
            ),
            seed_pizzerias_uc=storage_use_cases.SeedPizzeriasWebpagesRatingsUseCase(
                pizzeria_repository=pizzeria_repo,
            ),
        ),
        scrape_webpages_uc=use_cases.ScrapeWebpagesUseCase(
            get_webpages_uc=storage_use_cases.GetWebpagesUseCase(
                pizza_repository=pizzeria_repo,
            ),
            scrape_uc=scrape_uc,
            store_html_uc=storage_use_cases.StoreWebpageHtmlUseCase(
                html_repository=html_repo,
            ),
            mark_scraped_uc=storage_use_cases.MarkWebpageAsScrapedUseCase(
                pizza_repository=pizzeria_repo,
            ),
        ),
        parse_webpages_uc=use_cases.ParseWebpagesUseCase(
            get_webpages_uc=storage_use_cases.GetWebpagesUseCase(
                pizza_repository=pizzeria_repo,
            ),
            get_html_uc=storage_use_cases.GetWebpageHtmlUseCase(
                html_repository=html_repo,
            ),
            parse_pizzeria_uc=parse_pizzeria_uc,
            enrich_geo_uc=enrich_geo_uc,
            mark_parsed_uc=storage_use_cases.MarkWebpageAsParsedUseCase(
                pizza_repository=pizzeria_repo,
            ),
            seed_location_uc=storage_use_cases.SeedLocationUseCase(
                pizzeria_repository=pizzeria_repo,
            ),
        ),
    )


AddCategoryUCDep = Annotated[use_cases.AddCategoryUseCase, Depends(get_add_category_uc)]
