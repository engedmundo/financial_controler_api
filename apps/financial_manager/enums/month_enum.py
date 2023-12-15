from django.db import models


class MonthEnum(models.TextChoices):
    JANUARY = "january", "Janeiro"
    FEBRUARY = "february", "Fevereiro"
    MARCH = "march", "Março"
    APRIL = "april", "Abril"
    MAY = "may", "Maio"
    JUNE = "june", "Junho"
    JULY = "july", "Julho"
    AUGUST = "august", "Agosto"
    SEPTEMBER = "september", "Setembro"
    OCTOBER = "october", "Outubro"
    NOVEMBER = "november", "Novembro"
    DECEMBER = "december", "Dezembro"