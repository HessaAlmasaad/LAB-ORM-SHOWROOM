from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from .models import Car, Color,Review
from brands.models import Brand
from .forms import CarForm,ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def all_cars(request):
    query = request.GET.get('q', '')  # Search query
    brand_filter = request.GET.get('brand', '')  # Filter by brand
    color_filter = request.GET.get('color', '')  # Filter by color

    cars = Car.objects.all()

    # Filter by search query
    if query:
        cars = cars.filter(name__icontains=query)

    # Filter by brand
    if brand_filter:
        cars = cars.filter(brand__id=brand_filter)

    # Filter by color
    if color_filter:
        cars = cars.filter(colors__id=color_filter)

    # Paginate results
    paginator = Paginator(cars, 10)  # 10 cars per page
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)

    brands = Brand.objects.all()
    colors = Color.objects.all()

    return render(request, 'cars/all_cars.html', {
        'cars': cars,
        'brands': brands,
        'colors': colors,
        'query': query,
        'brand_filter': brand_filter,
        'color_filter': color_filter,
    })

@login_required
def create_car(request):
    # Debugging line: Check if the user is staff
    print(f"User is staff: {request.user.is_staff}")  # For debugging
    # Check if the user is either a superuser or staff
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Only admins and staff can add cars.", "alert-warning")
        return redirect("main:index_view")

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Car has been successfully added!")
            return redirect('cars:all_cars')
        else:
            messages.error(request, "Error adding car. Please check the form.")
    else:
        form = CarForm()
    
    return render(request, 'cars/create_car.html', {'form': form})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()  # Get all reviews for this car
    review_form = None

    if request.user.is_authenticated:
        review_form = ReviewForm()

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user  # Associate the review with the logged-in user
                review.car = car  # Associate the review with the car
                review.save()
                return redirect('cars:car_detail', car_id=car.id)  # Redirect to avoid resubmitting on refresh

    return render(request, 'cars/car_detail.html', {'car': car, 'reviews': reviews, 'review_form': review_form})

def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
 # Check if the user is either a superuser or staff
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Only admins and staff can add cars.", "alert-warning")
        return redirect("main:index_view")
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Car has been successfully updated!")
            return redirect('cars:car_detail', car_id=car.id)
        else:
            messages.error(request, "Error updating car. Please check the form.")
    else:
        form = CarForm(instance=car)
    
    return render(request, 'cars/update_car.html', {'form': form, 'car': car})

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Check if the user is either a superuser or staff
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Only admins and staff can add cars.", "alert-warning")
        return redirect("main:index_view")

    if request.method == 'POST':
        car_name = car.name
        car.delete()
        messages.success(request, f"Car '{car_name}' has been successfully deleted!")
        return redirect('cars:all_cars')
    
    return render(request, 'cars/delete_car.html', {'car': car})



