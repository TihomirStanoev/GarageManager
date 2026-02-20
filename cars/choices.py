from django.db import models


class BrandChoice(models.TextChoices):
    AUDI = 'Audi', 'Audi'
    BMW = 'BMW', 'BMW'
    VOLVO = 'Volvo', 'Volvo'
    MERCEDES = 'Mercedes', 'Mercedes'
    VOLKSWAGEN = 'Volkswagen', 'Volkswagen'


class EngineChoice(models.TextChoices):
    GASOLINE = 'gasoline', 'Gasoline'
    DIESEL = 'diesel', 'Diesel'
    HYBRID = 'hybrid', 'Hybrid'
    ELECTRIC = 'electric', 'Electric'
    LPG = 'lpg', 'LPG'