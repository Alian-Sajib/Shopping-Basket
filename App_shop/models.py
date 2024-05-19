from django.db import models

# Create your models here.

class Catagory(models.Model):
    title = models.CharField(max_length=264)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Catagories' # overwrite the model name in admin panel

class Product(models.Model):
    mainimage = models.ImageField(upload_to='products')
    name = models.CharField(max_length=264)
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE,related_name='catagory')
    preview_text = models.TextField(max_length=264,verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000,verbose_name='Description')
    price  = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']
    
    