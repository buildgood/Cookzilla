from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from django.db.models import Q, Avg
from itertools import chain
from datetime import datetime
from .forms import UserForm, UpdateUserForm, UpdateProfileForm
from .forms import ReviewForm, ReportForm, ImageForm, RecipeForm
from .models import Recipe, Ingredient, Rec_Ingre
from .models import Tag, Rec_Tag, Review, Relation
from .models import Group, Member, Event, Rsvp, Report
from .models import Rec_Image, Rev_Image, Rep_Image

def index(request):
    if request.user.is_authenticated():
        all_recipe = Recipe.objects.all()
        all_tag = Tag.objects.all()
        return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})
    else:
        return render(request, 'cook/index.html')

def recipe(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_recipe = Recipe.objects.all()
        all_tag = Tag.objects.all()
        return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})

def group(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_group = Group.objects.all()
        return render(request, 'cook/group.html', {'all_group': all_group})

def event(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_event = Event.objects.all()
        return render(request, 'cook/event.html', {'all_event': all_event})

def a_recipe(request, recipe_rid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        RevFormSet = modelformset_factory(Rev_Image, form=ImageForm, extra=3)

        if request.method == 'POST':
            print(request.POST)
            review_form = ReviewForm(request.POST)
            form_set = RevFormSet(request.POST, request.FILES, queryset=Rev_Image.objects.none())

            if review_form.is_valid() and form_set.is_valid():
                review = review_form.save(commit=False)
                review.rid = Recipe.objects.get(rid=recipe_rid)
                review.username = request.user
                review.save()

                for form in form_set.cleaned_data:
                    try:
                        image = form['img']
                        photo = Rev_Image(revid=review, img=image)
                        photo.save()
                    except KeyError, e:
                        pass

        formset = RevFormSet(queryset=Rev_Image.objects.none())
        one_recipe = get_object_or_404(Recipe, pk=recipe_rid)
        all_ingre = Rec_Ingre.objects.filter(rid__rid = recipe_rid).select_related()
        all_tag = Tag.objects.filter(rec_tag__rid = recipe_rid).select_related()
        all_relate = Relation.objects.filter(rid__rid = recipe_rid).select_related()
        all_review = Review.objects.filter(rid__rid = recipe_rid).select_related()
        recipe_img = Rec_Image.objects.filter(rid__rid=recipe_rid)
        review_img = Rev_Image.objects.filter(revid__rid=recipe_rid)
        rating = all_review.aggregate(Avg('rating')).values()[0]
        return render(request, 'cook/a_recipe.html', {'one_recipe': one_recipe, 'all_ingre': all_ingre, 'all_tag': all_tag, 'all_relate': all_relate, 'all_review': all_review, 'formset': formset, 'recipe_img':recipe_img, 'review_img': review_img, 'rating': rating})

def a_group(request, group_gid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        one_group = get_object_or_404(Group, pk=group_gid)
        all_member = Member.objects.filter(gid__gid=group_gid).select_related()
        all_event = Event.objects.filter(Q(gid__gid=group_gid) & Q(time__gte=datetime.now())).select_related()
        try:
            member = Member.objects.get(gid__gid=group_gid, username__username=request.user.username)
        except Member.DoesNotExist:
            member = None
        return render(request, 'cook/a_group.html', {'one_group': one_group, 'all_member': all_member, 'member': member, 'all_event': all_event})

def join_group(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        if request.method == "POST":
            gid = request.POST['group_gid']
            username = request.user.username
            group = get_object_or_404(Group, gid=gid)
            q=Member(gid=group, username=request.user)
            q.save()
            member = Member.objects.filter(gid__gid=q.gid.gid, username__username=username)
            all_member = Member.objects.filter(gid__gid=gid).select_related()
            all_event = Event.objects.filter(gid__gid=gid, time__gte=datetime.now()).select_related()
            return render(request, 'cook/a_group.html', {'one_group': q.gid, 'all_member': all_member, 'member': member, 'all_event': all_event})
        return render(request, 'cook/login.html')

def delete_group(request, group_gid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        q=Member.objects.filter(gid__gid=group_gid, username__username=request.user.username)
        q.delete()
        one_group = get_object_or_404(Group, pk=group_gid)
        all_member = Member.objects.filter(gid__gid=group_gid).select_related()
        all_event = Event.objects.filter(Q(gid__gid=group_gid) & Q(time__gte=datetime.now())).select_related()
        try:
            member = Member.objects.get(gid__gid=group_gid, username__username=request.user.username)
        except Member.DoesNotExist:
            member = None
        return render(request, 'cook/a_group.html', {'one_group': one_group, 'all_member': all_member, 'member': member, 'all_event': all_event})

def a_event(request, event_eid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        RepFormSet = modelformset_factory(Rep_Image, form=ImageForm, extra=3)

        if request.method == 'POST':
            report_form = ReportForm(request.POST)
            form_set = RepFormSet(request.POST, request.FILES, queryset=Rep_Image.objects.none())

            if report_form.is_valid() and form_set.is_valid():
                report = report_form.save(commit=False)
                report.eid = Event.objects.get(eid=event_eid)
                report.username = Rsvp.objects.get(eid__eid=event_eid, username__username__username=request.user.username)
                report.save()

                for form in form_set.cleaned_data:
                    try:
                        image = form['img']
                        photo = Rep_Image(repid=report, img=image)
                        photo.save()
                    except KeyError, e:
                        pass

        formset = RepFormSet(queryset=Rep_Image.objects.none())
        one_event = get_object_or_404(Event, pk=event_eid)
        one_group = one_event.gid
        all_report = Report.objects.filter(eid=event_eid).select_related()
        all_img = Rep_Image.objects.filter(repid__eid=event_eid)
        try:
            member = Member.objects.get(gid__gid=one_group.gid, username__username=request.user.username)
        except Member.DoesNotExist:
            member = None

        try:
            rsvp = Rsvp.objects.get(eid__eid=event_eid, username__username__username=request.user.username)
        except Rsvp.DoesNotExist:
            rsvp = None
        return render(request, 'cook/a_event.html', {'one_event': one_event, 'one_group': one_group, 'all_report': all_report, 'member':member, 'rsvp': rsvp, 'formset': formset, 'all_img': all_img})

def rsvp(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        if request.method == "POST":
            eid = request.POST['event_eid']
            username = request.user.username
            event = get_object_or_404(Event, eid=eid)
            memberof = get_object_or_404(Member, username=request.user)
            q=Rsvp(eid=event, username=memberof)
            q.save()
            all_report = Report.objects.filter(eid=eid).select_related()
            member = Member.objects.filter(gid__gid=q.eid.gid.gid, username__username=username)
            return render(request, 'cook/a_event.html', {'one_event': q.eid, 'one_group': q.eid.gid, 'all_report': all_report, 'member': member, 'rsvp': q})
        return render(request, 'cook/login.html')

def delete_rsvp(request, event_eid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        q=Rsvp.objects.filter(eid__eid=event_eid, username__username__username=request.user.username)
        q.delete()
        one_event = get_object_or_404(Event, pk=event_eid)
        one_group = one_event.gid
        all_report = Report.objects.filter(eid=event_eid).select_related()
        try:
            member = Member.objects.get(gid__gid=one_group.gid, username__username=request.user.username)
        except Member.DoesNotExist:
            member = None

        try:
            rsvp = Rsvp.objects.get(eid__eid=event_eid, username__username__username=request.user.username)
        except Rsvp.DoesNotExist:
            rsvp = None
        RepFormSet = modelformset_factory(Rep_Image, form=ImageForm, extra=3)
        formset = RepFormSet(queryset=Rep_Image.objects.none())
        return render(request, 'cook/a_event.html', {'one_event': one_event, 'one_group': one_group, 'all_report': all_report, 'member':member, 'rsvp': rsvp, 'formset': formset})

def login_user(request):
    if request.user.is_authenticated():
        all_recipe = Recipe.objects.all()
        all_tag = Tag.objects.all()
        return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['login'] = username
                    request.session.save()
                    all_recipe = Recipe.objects.all()
                    all_tag = Tag.objects.all()

                    return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})
                else:
                    return render(request, 'cook/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'cook/login.html', {'error_message': 'Invalid login'})
        return render(request, 'cook/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'cook/index.html')

def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render(request, 'cook/recipe.html')
	return render(request, 'cook/login.html')

def search(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        if request.method == "POST":
            type = request.POST['type']
            content = request.POST['content']
            if content is not None:
                if type == "recipe":
                    tags = Recipe.objects.filter(rec_tag__tid__tag__icontains=content)
                    recipes = Recipe.objects.filter(Q(steps__icontains=content) | Q(title__icontains=content))
                    all_recipe = chain(tags, recipes)
                    all_tag = Tag.objects.all()
                    return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})
                elif type == "group":
                    all_group = Group.objects.filter(Q(name__icontains=content) | Q(description__icontains=content))
                    return render(request, 'cook/group.html', {'all_group': all_group})
                elif type == "event":
                    all_event = Event.objects.filter(Q(description__icontains=content) | Q(title__icontains=content))
                    return render(request, 'cook/event.html', {'all_event': all_event})
        all_recipe = Recipe.objects.all()
        return render(request, 'cook/recipe.html', {'all_recipe': all_recipe})

def search_tag(request, tag_tag):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_recipe = Recipe.objects.filter(rec_tag__tid__tag=tag_tag)
        all_tag = Tag.objects.all()
        return render(request, 'cook/recipe.html', {'all_recipe': all_recipe, 'all_tag': all_tag})

def account(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_recipe = Recipe.objects.filter(username__username=request.user.username).select_related()
        all_review = Review.objects.filter(username__username=request.user.username).select_related()
        all_group = Group.objects.filter(member__username__username=request.user.username).select_related()
        all_rsvp = Event.objects.filter(rsvp__username__username__username=request.user.username).select_related()
        all_report = Report.objects.filter(username__username__username__username=request.user.username).select_related()
        return render(request, 'cook/account.html', {'all_recipe': all_recipe, 'all_review': all_review, 'all_group': all_group, 'all_rsvp': all_rsvp, 'all_report': all_report})

def my_recipe(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_recipe = Recipe.objects.filter(username__username=request.user.username).select_related()
        return render(request, 'cook/my_recipe.html', {'all_recipe': all_recipe})

def delete_recipe(request, recipe_rid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        q=Recipe.objects.filter(rid=recipe_rid)
        q.delete()
        all_recipe = Recipe.objects.filter(username__username=request.user.username).select_related()
        return render(request, 'cook/my_recipe.html', {'all_recipe': all_recipe})

def my_group(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_group = Group.objects.filter(member__username__username=request.user.username).select_related()
        return render(request, 'cook/my_group.html', {'all_group': all_group})

def my_rsvp(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_rsvp = Event.objects.filter(rsvp__username__username__username=request.user.username).select_related()
        return render(request, 'cook/my_rsvp.html', {'all_rsvp': all_rsvp})

def my_review(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_review = Review.objects.filter(username__username=request.user.username).select_related()
        all_img = Rev_Image.objects.filter(revid__username__username=request.user.username).select_related()
        return render(request, 'cook/my_review.html', {'all_review': all_review, 'all_img': all_img})

def delete_review(request, review_revid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        q=Review.objects.filter(revid=review_revid)
        q.delete()
        all_review = Review.objects.filter(username__username=request.user.username).select_related()
        return render(request, 'cook/my_review.html', {'all_review': all_review})

def my_report(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        all_report = Report.objects.filter(username__username__username__username=request.user.username).select_related()
        all_img = Rep_Image.objects.filter(repid__username__username__username__username=request.user.username).select_related()
        return render(request, 'cook/my_report.html', {'all_report': all_report, 'all_img': all_img})

def delete_report(request, report_repid):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        q=Report.objects.filter(repid=report_repid)
        q.delete()
        all_report = Report.objects.filter(username__username__username__username=request.username).select_related()
        return render(request, 'cook/my_report.html', {'all_report': all_report})

def my_profile(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        return render(request, 'cook/my_profile.html')

def update_user(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        if request.method == 'POST':
            print(request.POST)
            form_user = UpdateUserForm(data=request.POST, instance=request.user)
            if form_user.is_valid():
                form_user.save()

            form_profile = UpdateProfileForm(request.POST, instance=request.user.profile)
            if form_profile.is_valid():
                form_profile.save()

        return render(request, 'cook/my_profile.html')

def add_recipe(request):
    if not request.user.is_authenticated():
        return render(request, 'cook/login.html')
    else:
        RecFormSet = modelformset_factory(Rec_Image, form=ImageForm, extra=3)

        if request.method == 'POST':
            recipe_form = RecipeForm(request.POST)
            form_set_img = RecFormSet(request.POST, request.FILES, queryset=Rec_Image.objects.none())

            ingre = request.POST.get('ingredient', '')
            tag = request.POST.get('tag', '')

            if recipe_form.is_valid() and form_set_img.is_valid():
                print(request.POST)
                recipe = recipe_form.save(commit=False)
                recipe.username = request.user
                recipe.save()

                for ingre_line in ingre.split('\n'):
                    line = ingre_line.split(' ')
                    print(line[0])
                    try:
                        ingre_object = Ingredient.objects.get(ingredient=line[0])
                    except Ingredient.DoesNotExist:
                        ingre_object = None
                    if ingre_object is None:
                        q_ingre=Ingredient(ingredient=line[0])
                        q_ingre.save()
                    else:
                        q_ingre = ingre_object
                    quan = float(line[1])
                    q_rec_ingre=Rec_Ingre(rid=recipe, iid=q_ingre, quantities=quan)
                    q_rec_ingre.save()

                for tag_line in tag.split(' '):
                    try:
                        tag_object = Tag.objects.get(tag=tag_line)
                    except Tag.DoesNotExist:
                        tag_object = None
                    if tag_object is None:
                        q_tag = Tag(tag=tag_line)
                        q_tag.save()
                    else:
                        q_tag = tag_object
                    q_rec_tag = Rec_Tag(rid=recipe, tid=q_tag)
                    q_rec_tag.save()


                for form in form_set_img.cleaned_data:
                    try:
                        image = form['img']
                        photo = Rec_Image(rid=recipe, img=image)
                        photo.save()
                    except KeyError, e:
                        pass

        formset_img = RecFormSet(queryset=Rec_Image.objects.none())
        return render(request, 'cook/add_recipe.html', {'formset_img': formset_img})

