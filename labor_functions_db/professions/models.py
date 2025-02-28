from django.db import models

class Profession(models.Model):
    name = models.CharField(max_length=255)
    okpdtr_code = models.CharField(max_length=20)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class GeneralizedLaborFunction(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        default="TEMP_CODE"
        )
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class LaborFunction(models.Model):
    name = models.CharField(max_length=255)
    qualification_level = models.IntegerField(choices=[(6, 'Уровень 6'), (7, 'Уровень 7')])
    generalized_function = models.ForeignKey(GeneralizedLaborFunction, on_delete=models.CASCADE, null=True, blank=True) #FIXME
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Уровень {self.qualification_level})" 
    
class LaborAction(models.Model):
    description = models.TextField()
    labor_function = models.ForeignKey(LaborFunction, on_delete=models.CASCADE)

class RequiredSkill(models.Model):
    description = models.TextField()
    labor_function = models.ForeignKey(LaborFunction, on_delete=models.CASCADE)

class RequiredKnowledge(models.Model):
    description = models.TextField()
    labor_function = models.ForeignKey(LaborFunction, on_delete=models.CASCADE)


class OKSO(models.Model):
    code = models.CharField(max_length=20)
    labor_function = models.ForeignKey(
        LaborFunction, 
        on_delete=models.CASCADE, 
        null=True,  
        blank=True  
    )

    def __str__(self):
        return self.code