"""Router for category management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from geolocation import GeolocationService
from geolocation.application import use_cases as geo_use_cases
from pizza_data_collector import models as collector_models, parsers, scrapers
from pizza_data_collector.application import use_cases as collector_use_cases
from pizza_data_storage import repositories as storage_repos
from pizza_data_storage.application import use_cases as storage_use_cases

from pizza_api.application.use_cases import (
    AddCategoryUseCase,
    ParseEditionsUseCase,
    ParseWebpagesUseCase,
    ScrapeEditionsUseCase,
    ScrapeWebpagesUseCase,
)
from pizza_api.dependencies.repositories import get_html_repo, get_pizzeria_repo, get_ranking_repo
from pizza_api.schemas.requests import CategoryCreateRequest
from pizza_api.schemas.responses import AddCategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

RankingRepoDep = Annotated[storage_repos.RankingsRepository, Depends(get_ranking_repo)]
PizzeriaRepoDep = Annotated[storage_repos.PizzeriaRepository, Depends(get_pizzeria_repo)]
HtmlRepoDep = Annotated[storage_repos.HtmlStorageRepository, Depends(get_html_repo)]


def get_add_category_uc(
    ranking_repo: RankingRepoDep,
    pizzeria_repo: PizzeriaRepoDep,
    html_repo: HtmlRepoDep,
) -> AddCategoryUseCase:
    """Build and wire the AddCategoryUseCase with all its dependencies."""
    scrape_uc = collector_use_cases.ScrapeUseCase(
        scraper=scrapers.Scraper(http_client=scrapers.HttpClient())
    )
    parse_edition_uc = collector_use_cases.ParseEditionUseCase(
        parser=parsers.EditionParser(
            awards_patterns=collector_models.award_name_patterns,
            card_patterns=collector_models.card_patterns,
            url_pattern=collector_models.url_pattern,
            position_patterns=collector_models.ranking_position_patterns,
        )
    )
    parse_pizzeria_uc = collector_use_cases.ParsePizzeriaUseCase(
        parser=parsers.PizzeriaParser(
            coord_patterns=collector_models.coordinate_patterns,
            address_patterns=collector_models.adress_patterns,
            phone_patterns=collector_models.phone_patterns,
        )
    )
    enrich_geo_uc = geo_use_cases.EnrichGeolocationUseCase(
        geolocation_service=GeolocationService(user_agent="best-pizza-services/1.0")
    )

    return AddCategoryUseCase(
        seed_uc=storage_use_cases.SeedCategoriesAndEditionsUseCase(
            ranking_repository=ranking_repo,
        ),
        scrape_editions_uc=ScrapeEditionsUseCase(
            get_editions_uc=storage_use_cases.GetEditionsUseCase(ranking_repository=ranking_repo),
            scrape_uc=scrape_uc,
            store_html_uc=storage_use_cases.StoreEditionHtmlUseCase(html_repository=html_repo),
            mark_scraped_uc=storage_use_cases.MarkEditionAsScrapedUseCase(ranking_repository=ranking_repo),
        ),
        parse_editions_uc=ParseEditionsUseCase(
            get_editions_uc=storage_use_cases.GetEditionsUseCase(ranking_repository=ranking_repo),
            html_exists_uc=storage_use_cases.EditionHtmlExistsUseCase(html_repository=html_repo),
            get_html_uc=storage_use_cases.GetEditionHtmlUseCase(html_repository=html_repo),
            parse_edition_uc=parse_edition_uc,
            mark_parsed_uc=storage_use_cases.MarkEditionAsParsedUseCase(ranking_repository=ranking_repo),
            seed_pizzerias_uc=storage_use_cases.SeedPizzeriasWebpagesRatingsUseCase(
                pizzeria_repository=pizzeria_repo,
            ),
        ),
        scrape_webpages_uc=ScrapeWebpagesUseCase(
            get_webpages_uc=storage_use_cases.GetWebpagesUseCase(pizza_repository=pizzeria_repo),
            scrape_uc=scrape_uc,
            store_html_uc=storage_use_cases.StoreWebpageHtmlUseCase(html_repository=html_repo),
            mark_scraped_uc=storage_use_cases.MarkWebpageAsScrapedUseCase(pizza_repository=pizzeria_repo),
        ),
        parse_webpages_uc=ParseWebpagesUseCase(
            get_webpages_uc=storage_use_cases.GetWebpagesUseCase(pizza_repository=pizzeria_repo),
            html_exists_uc=storage_use_cases.WebpageHtmlExistsUseCase(html_repository=html_repo),
            get_html_uc=storage_use_cases.GetWebpageHtmlUseCase(html_repository=html_repo),
            parse_pizzeria_uc=parse_pizzeria_uc,
            enrich_geo_uc=enrich_geo_uc,
            mark_parsed_uc=storage_use_cases.MarkWebpageAsParsedUseCase(pizza_repository=pizzeria_repo),
            seed_location_uc=storage_use_cases.SeedLocationUseCase(pizzeria_repository=pizzeria_repo),
        ),
    )


AddCategoryUCDep = Annotated[AddCategoryUseCase, Depends(get_add_category_uc)]


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=AddCategoryResponse,
    summary="Add a new category and run the full scrape + parse cycle",
)
def add_category(
    body: CategoryCreateRequest,
    use_case: AddCategoryUCDep,
) -> AddCategoryResponse:
    """Seed a new category, scrape all its editions and pizzeria webpages, and parse the results."""
    result = use_case.execute(category_schemas=body.categories)
    return AddCategoryResponse.model_validate(result, from_attributes=True)
