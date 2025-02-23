from django.db import models

class Profession(models.Model):
    name = models.CharField(max_length=255)
    okpdtr_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class GeneralizedLaborFunction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class LaborFunction(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    qualification_level = models.IntegerField()
    generalized_function = models.ForeignKey(GeneralizedLaborFunction, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name}"

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
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)