from enum import Enum

class VideoSource(str, Enum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"

class Category(str, Enum):
    RECETAS = "recetas"
    FITNESS = "fitness"
    VIAJES = "viajes"
    EDUCACION = "educacion"
    ENTRETENIMIENTO = "entretenimiento"
    NEGOCIOS = "negocios"
    TECNOLOGIA = "tecnologia"
    OTROS = "otros"
