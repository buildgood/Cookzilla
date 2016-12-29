from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

@python_2_unicode_compatible
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	introduction = models.CharField(max_length=1000, blank=True)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

	def __str__(self):
		return self.user.username

@python_2_unicode_compatible
class Recipe(models.Model):
	rid = models.AutoField(primary_key=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	servings = models.IntegerField()
	steps = models.CharField(max_length=2000)

	def __str__(self):
		return self.title+'-'+self.username.username

@python_2_unicode_compatible
class Ingredient(models.Model):
	iid = models.AutoField(primary_key=True)
	ingredient = models.CharField(max_length=40)

	def __str__(self):
		return self.ingredient

@python_2_unicode_compatible
class Standard_quan(models.Model):
	qid = models.AutoField(primary_key=True)
	quantities = models.DecimalField(max_digits=6, decimal_places=2)
	unit = models.CharField(max_length=50)

	def __str__(self):
		return self.unit

@python_2_unicode_compatible
class Rec_Ingre(models.Model):
	rid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	iid = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	quantities = models.DecimalField(max_digits=6, decimal_places=2)

	class Meta:
		unique_together = (('rid', 'iid'),)

	def __str__(self):
		return str(self.rid)+"-"+str(self.iid)

@python_2_unicode_compatible
class Relation(models.Model):
	rid = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rid_prev')
	relatedrid = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rid_next')

	class Meta:
		unique_together = (('rid', 'relatedrid'),)

	def __str__(self):
		return str(self.rid)+"-"+str(self.relatedrid)

@python_2_unicode_compatible
class Tag(models.Model):
	tid = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=40)

	def __str__(self):
		return self.tag

@python_2_unicode_compatible
class Rec_Tag(models.Model):
	rid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	tid = models.ForeignKey(Tag, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('rid', 'tid'),)

	def __str__(self):
		return str(self.rid)+"-"+str(self.tid)

@python_2_unicode_compatible
class Review(models.Model):
	revid = models.AutoField(primary_key=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE)
	rid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=1000)
	suggestion = models.CharField(max_length=500)
	rating = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

@python_2_unicode_compatible
class Group(models.Model):
	gid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=3000)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Member(models.Model):
	gid = models.ForeignKey(Group, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('gid', 'username'),)

	def __str__(self):
		return str(self.gid)+"-"+str(self.username)

@python_2_unicode_compatible
class Event(models.Model):
	eid = models.AutoField(primary_key=True)
	gid = models.ForeignKey(Group, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	time = models.DateTimeField()
	location = models.CharField(max_length=100)
	description = models.CharField(max_length=3000)

	def __str__(self):
		return self.title

@python_2_unicode_compatible
class Rsvp(models.Model):
	eid = models.ForeignKey(Event, on_delete=models.CASCADE)
	username = models.ForeignKey(Member, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('eid', 'username'),)

	def __str__(self):
		return str(self.eid)+"-"+str(self.username)

@python_2_unicode_compatible
class Report(models.Model):
	repid = models.AutoField(primary_key=True)
	eid = models.ForeignKey(Event, on_delete=models.CASCADE)
	username = models.ForeignKey(Rsvp, on_delete=models.CASCADE)
	description = models.CharField(max_length=3000)
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.repid)

def upload_recipe(instance, filename):
	return 'recipe/%s/%s' % (instance.rid.rid, filename)

def upload_review(instance, filename):
	return 'review/%s/%s' % (instance.revid.revid, filename)

def upload_report(instance, filename):
	return 'report/%s/%s' % (instance.repid.repid, filename)

@python_2_unicode_compatible
class Rec_Image(models.Model):
	rid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	img = models.FileField(upload_to=upload_recipe)

	class Meta:
		unique_together = (('rid', 'img'),)

	def __str__(self):
		return str(self.rid.rid)

@python_2_unicode_compatible
class Rev_Image(models.Model):
	revid = models.ForeignKey(Review, on_delete=models.CASCADE)
	img = models.FileField(upload_to=upload_review)

	class Meta:
		unique_together = (('revid', 'img'),)

	def __str__(self):
		return str(self.revid.revid)

@python_2_unicode_compatible
class Rep_Image(models.Model):
	repid = models.ForeignKey(Report, on_delete=models.CASCADE)
	img = models.FileField(upload_to=upload_report)

	class Meta:
		unique_together = (('repid', 'img'),)

	def __str__(self):
		return str(self.repid.repid)