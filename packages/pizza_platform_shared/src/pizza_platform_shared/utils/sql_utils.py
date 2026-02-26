"""SQL utility functions for the pizza platform shared codebase."""

def get_pizza_query(self) -> sa.Select[Any]:
        return sa.select(
            models.Pizzerias.name,
            models.Locations.latitude,
            models.Locations.longitude,
        ).join(
            models.Locations,
            models.Locations.pizzeria_id == models.Pizzerias.id,
        ).where(
            models.Locations.latitude.is_not(None)
            & models.Locations.longitude.is_not(None)
        ).order_by(models.Pizzerias.name)