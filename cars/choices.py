from django.db import models


class BrandChoice(models.TextChoices):
    AUDI = 'audi', 'Audi'
    BMW = 'bmw', 'BMW'
    VOLVO = 'volvo', 'Volvo'
    MERCEDES = 'mercedes', 'Mercedes'
    VOLKSWAGEN = 'volkswagen', 'Volkswagen'


class EngineChoice(models.TextChoices):
    GASOLINE = 'gasoline', 'Gasoline'
    DIESEL = 'diesel', 'Diesel'
    HYBRID = 'hybrid', 'Hybrid'
    ELECTRIC = 'electric', 'Electric'
    LPG = 'lpg', 'LPG'