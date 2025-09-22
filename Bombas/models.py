from django.db import models

class Mode(models.Model):
    MODES = [
        ("none", "Nenhum"),
        ("ronaldo", "Bomba do Ronaldo"),
        ("nene", "Bomba do Seu Nenê"),
        ("eber", "Bomba do Eber/Abel"),
    ]
    mode = models.CharField(max_length=20, choices=MODES, default="none")
    def __str__(self):
        return self.get_mode_display()
# Create your models here.
