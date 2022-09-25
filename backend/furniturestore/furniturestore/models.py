from djongo import models
#Models are here
#Support models are for mongoDB object like Array's and Embedded Documents

#Furniture Suppport models are here -->


class ratingsArray(models.Model):
    _id= models.ObjectIdField()
    userId= models.CharField(max_length=200,null=True)
    rating= models.FloatField(max_length=200)
    class Meta:
        abstract = True
class ratings(models.Model):   
    medianValueRating=models.FloatField(max_length=200)
    ratingsArray =models.ArrayField(model_container=ratingsArray,default=[])
    class Meta:
        abstract = True
class categoryArray(models.Model):
    data= models.CharField(max_length=200)

    class Meta:
        abstract = True
class materialArray(models.Model):
    data= models.CharField(max_length=200)

    class Meta:
        abstract = True
        
#Furniture support models end here <--
class Furniture(models.Model):
    _id = models.ObjectIdField()
    name= models.CharField(max_length=200,default="")
    hasWarranty = models.BooleanField(default=True)
    isPopular = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=1.0)
    quantity = models.IntegerField(default=1)
    stock = models.BooleanField(default=True)
    description = models.TextField(max_length=1000,default="")
    categoryArray = models.ArrayField(model_container=categoryArray,null=True)
    materialArray = models.ArrayField(model_container=materialArray,null=True)
    ratings =models.EmbeddedField(model_container=ratings,null=True) 
    
    def __str__(self):
        return self.name
    objects = models.DjongoManager()
#ORDER Suppport models are here -->
class items(models.Model):
    _id= models.CharField(max_length=200)

    class Meta:
        abstract = True
        

#Order support models end here <--
class Order(models.Model):
    _id = models.ObjectIdField()
    items= models.ArrayField( model_container=items,null=True)
    userId = models.CharField(max_length=200,default="")
    totalValue = models.FloatField(max_length=200,default=0)
    sent = models.CharField(max_length=200,default="")
    delivered = models.CharField(max_length=200,default="")
    ordered =models.CharField(max_length=200,default="")
    message = models.TextField(max_length=1024,default='No message')
    orderPaid =models.BooleanField(default=False)
    paypalOrderId = models.CharField(max_length=300,default="")
    

    def __str__(self):
        return self.headline
    objects = models.DjongoManager()
#User Suppport models are here -->
class ordersArrays(models.Model):
    _id= models.CharField(max_length=200)

    class Meta:
        abstract = True
class cartArrays(models.Model):
    _id= models.CharField(max_length=200)

    class Meta:
        abstract = True
#User support models end here <--
class User(models.Model):
    _id = models.ObjectIdField()
    email = models.EmailField(max_length=100)
    username= models.CharField(max_length=200,default=' ')
    password = models.CharField(max_length=1000,default=' ')
    address= models.CharField(max_length=2000,default=' ')
    cart=models.ArrayField(model_container=cartArrays,null=True)
    orders=models.ArrayField(model_container=ordersArrays,null=True)
    emailConfirmed= models.BooleanField(default=False)
    confirmationString = models.CharField(max_length=1000,default=' ')
    firstName= models.CharField(max_length=200,default=' ')
    lastName = models.CharField(max_length=200,default=' ')
    role= models.CharField(max_length=15,default=' ')
    phone = models.CharField(max_length=15,default=' ')

    objects = models.DjongoManager()