from django.db import models

# Create your models here.
class Star_cast(models.Model):
	cast_name = models.CharField(max_length = 300, null = False)

	def __str__(self):
		return ("%s" % (self.cast_name))

class Director(models.Model):
	director = models.CharField(max_length = 300, null = False)

	def __str__(self):
		return ("%s" % (self.director))

class Movies(models.Model):
	title=models.CharField(max_length = 250)
	crew=models.TextField(null=True)
	year = models.CharField(max_length = 50)
	rating = models.CharField(max_length = 50)
	language = models.CharField(max_length = 50)
	cast = models.ForeignKey(Star_cast, on_delete = models.CASCADE, db_column="cast_name")
	director = models.ForeignKey(Director, on_delete = models.CASCADE, db_column="director")

	def y_o_r(self):
		return self.year

	y_o_r.short_description = 'year released?'

	def __str__(self):
		return ("%s" % (self.title))

