from django.db import models


class BrandChoice(models.TextChoices):
    AUDI = 'Audi', 'Audi'
    BMW = 'BMW', 'BMW'
    VOLVO = 'Volvo', 'Volvo'
    MERCEDES = 'Mercedes', 'Mercedes'
    VOLKSWAGEN = 'Volkswagen', 'Volkswagen'


class EngineChoice(models.TextChoices):
    GASOLINE = 'Gasoline', 'Gasoline'
    DIESEL = 'Diesel', 'Diesel'
    HYBRID = 'Hybrid', 'Hybrid'
    ELECTRIC = 'Electric', 'Electric'
    LPG = 'LPG', 'LPG'