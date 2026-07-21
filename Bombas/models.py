from django.db import models
from django.utils import timezone


class Mode(models.Model):

    MODES = [
        ("none", "Nenhum"),
        ("ronaldo", "Bomba do Ronaldo"),
        ("nene", "Bomba do Seu Nenê"),
        ("eber", "Bomba do Eber/Abel"),
    ]

    mode = models.CharField(
        max_length=20,
        choices=MODES,
        default="none"
    )

    last_ping = models.DateTimeField(
        default=timezone.now
    )

    # indica se o estado atual foi ativado
    # automaticamente pela programação
    auto_active = models.BooleanField(
        default=False
    )

    # Modo manual expira
    manual_until = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return self.get_mode_display()


class Schedule(models.Model):

    WEEKDAYS = [
        (0, "Segunda"),
        (1, "Terça"),
        (2, "Quarta"),
        (3, "Quinta"),
        (4, "Sexta"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    weekday = models.IntegerField(
        choices=WEEKDAYS
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        default="eber"
    )

    def __str__(self):

        return (
            f"{self.get_weekday_display()} - "
            f"{self.start_time} até {self.end_time}"
        )