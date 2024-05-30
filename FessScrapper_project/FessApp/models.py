from django.db import models

class DynamicCollectionModel(models.Model):
    article_link=models.CharField(max_length=4000)
    article_title = models.CharField(max_length=4000)
    article_publish_date = models.DateField()
    article_file_path = models.TextField()

    class Meta:
        abstract = True  # Make this model abstract

# Your specific model with additional fields
class FessModel(DynamicCollectionModel):
    pass
        



