from django.contrib import admin

from .models import Profile
from .models import Ingredient
from .models import Standard_quan
from .models import Recipe
from .models import Rec_Ingre
from .models import Relation
from .models import Tag
from .models import Rec_Tag
from .models import Review
from .models import Group
from .models import Member
from .models import Event
from .models import Rsvp
from .models import Report
from .models import Rec_Image
from .models import Rev_Image
from .models import Rep_Image


admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Standard_quan)
admin.site.register(Rec_Ingre)
admin.site.register(Relation)
admin.site.register(Tag)
admin.site.register(Rec_Tag)
admin.site.register(Review)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Rsvp)
admin.site.register(Report)
admin.site.register(Rec_Image)
admin.site.register(Rev_Image)
admin.site.register(Rep_Image)