from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):    
    category_list = Category.objects.all()
    page_list = Page.objects.all()

    for category in category_list:
        category.url = category.name.replace(' ', '_')

        for page in page_list:
            if category.name == page.category:
                category.views += page.views
    
    top5_categories = Category.objects.order_by('-views')[:5]

    context = {'categories': category_list,
                    'pages': page_list,
                    'top5_cats': top5_categories}

    return render(request, 'rango/index.html', context)

def about(request):
	context = {'about_filler': "This is what it's all about. Back to <a href='/rango/'>Index</a>"}
	return render(request, 'rango/about.html', context)

def category(request, category_name_url):
    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    context = {'category_name_url': category_name_url}
    category_name = category_name_url.replace('_', ' ')
    context['category_name'] = category_name    

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(name=category_name)

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context)

def add_category(request):
    # Get the context from the request
    #context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def decode_url(url):
    cat_name = url.replace('_', ' ')
    return cat_name

def add_page(request, category_name_url):
    category_name = decode_url(category_name_url)

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # Go back and render the add category form as a way of saying the category 
                return render(request, 'rango/add_category.html', {'test': test, 'foo': Category.objects.all()})

            page.views = 0
            page.save()

            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()
    return render(request, 'rango/add_page.html',
                    {'category_name_url': category_name_url,
                    'category_name': category_name,
                    'form': form})