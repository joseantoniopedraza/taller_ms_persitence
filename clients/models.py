from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Interests(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Clients_Interests(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interests, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.name} - {self.interest.name}"