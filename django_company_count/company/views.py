from django.shortcuts import render
from .forms import UploadFileForm,QueryForm
from .models import Company
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CompanySerializer
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import csv
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache
import threading
from django.contrib.auth.models import User
from django.db import transaction

# @login_required
# @api_view(['GET'])
# def company_list(request):
#     companies = Company.objects.all()
#     serializer = CompanySerializer(companies, many=True)
#     return Response(serializer.data)

# def check_insertion_progress(request, cache_key):
#     progress = cache.get(cache_key, 0)  # Default to 0 if not set
#     return JsonResponse({'progress': progress})



# def async_process_csv(file_path, cache_key, user):
#     try:
#         print(f"Processing file: {file_path}")

#         with open(file_path, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             companies = []
#             total_rows = sum(1 for _ in reader)
#             f.seek(0)  # Reset reader after counting rows
#             next(reader)  # Skip the header

#             # Increase batch size to optimize bulk inserts
#             batch_size = 20000  # Try higher batch sizes
#             with transaction.atomic():  # Wrap everything in a transaction for efficiency
#                 for i, row in enumerate(reader):
#                     # Handle 'year_founded', making sure it's a valid number
#                     year_founded = row.get('year founded', None)
#                     if year_founded:
#                         try:
#                             year_founded = int(float(year_founded))  # Convert to integer
#                         except ValueError:
#                             year_founded = None
#                     else:
#                         year_founded = None

#                     current_employee_estimate = row.get('current employee estimate', None)
#                     if not current_employee_estimate or not current_employee_estimate.strip().isdigit():
#                         current_employee_estimate = None

#                     total_employee_estimate = row.get('total employee estimate', None)
#                     if not total_employee_estimate or not total_employee_estimate.strip().isdigit():
#                         total_employee_estimate = None

#                     # Create the company object
#                     company = Company(
#                         user=user,  # Assign the current user to the company
#                         name=row.get('name', 'Unknown Name'),
#                         revenue=row.get('revenue', 0),
#                         domain=row.get('domain', None),
#                         year_founded=year_founded,
#                         industry=row.get('industry', None),
#                         size_range=row.get('size range', None),
#                         locality=row.get('locality', None),
#                         country=row.get('country', None),
#                         linkedin_url=row.get('linkedin url', None),
#                         current_employee_estimate=current_employee_estimate,
#                         total_employee_estimate=total_employee_estimate,
#                     )
#                     companies.append(company)

#                     # Insert in batches to optimize performance
#                     if len(companies) >= batch_size:
#                         Company.objects.bulk_create(companies, ignore_conflicts=True)
#                         companies.clear()

#                     # Update progress in cache
#                     cache.set(cache_key, (i + 1) / total_rows * 100)

#                 # Insert any remaining companies
#                 if companies:
#                     Company.objects.bulk_create(companies, ignore_conflicts=True)

#         # Remove the file after processing
#         os.remove(file_path)

#         # Mark as complete
#         cache.set(cache_key, 100)
#         print("Data inserted successfully.")
#     except Exception as e:
#         print(f"Error occurred during CSV processing: {e}")
#         cache.set(cache_key, -1)  # Mark as failed


# @login_required
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = request.FILES['file']

#             # Save the file temporarily
#             fs = FileSystemStorage()
#             filename = fs.save(csv_file.name, csv_file)
#             file_path = os.path.join(settings.MEDIA_ROOT, filename)

#             # Generate a cache key for tracking progress
#             cache_key = f'csv_progress_{request.user.id}_{filename}'

#             # Start processing CSV in a separate thread to avoid blocking
#             thread = threading.Thread(target=async_process_csv, args=(file_path, cache_key, request.user))
#             thread.start()

#             return JsonResponse({'cache_key': cache_key})
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})


# @login_required
# def query_builder(request):
#     # Query distinct values from the database
#     industries = Company.objects.filter(user=request.user).values_list('industry', flat=True).distinct()
#     size_ranges = Company.objects.filter(user=request.user).values_list('size_range', flat=True).distinct()
#     states = Company.objects.filter(user=request.user).values_list('locality', flat=True).distinct()
#     countries = Company.objects.filter(user=request.user).values_list('country', flat=True).distinct()
#     years_founded = Company.objects.filter(user=request.user).values_list('year_founded', flat=True).distinct()
    
#     # Create a list of employee ranges with 'from' and 'to' values
#     employee_counts = [
#         {'from': 1, 'to': 100},
#         {'from': 101, 'to': 200},
#         {'from': 201, 'to': 500},
#         {'from': 501, 'to': 1000},
#         {'from': 1001, 'to': 5000},
#         {'from': 5001, 'to': 10000},
#         {'from': 10001, 'to': 50000},
#         {'from': 50001, 'to': None},  # No upper bound for this range
#     ]

#     form = QueryForm(request.GET or None)
#     query = Company.objects.filter(user=request.user).only('name', 'industry', 'current_employee_estimate')

#     # Filter parameters
#     industry = request.GET.get('industry')
#     size_range = request.GET.get('size_range')
#     locality = request.GET.get('locality')
#     state = request.GET.get('state')
#     employees_from = request.GET.get('employees_from')
#     country = request.GET.get('country')
#     year_founded = request.GET.get('year_founded')

#     # Apply filters to the query
#     if industry:
#         query = query.filter(industry__icontains=industry)
#     if size_range:
#         query = query.filter(size_range__icontains=size_range)
#     if locality:
#         query = query.filter(locality__icontains=locality)
#     if state:
#         query = query.filter(address__icontains=state)
#     if employees_from:
#         query = query.filter(current_employee_estimate__gte=employees_from)
#     if country:
#         query = query.filter(country__icontains=country)
#     if year_founded:
#         query = query.filter(year_founded__icontains=year_founded)

#     results = query.count()

#     return render(request, 'query.html', {
#         'form': form,
#         'industries': industries,
#         'size_ranges': size_ranges,
#         'states': states,
#         'countries': countries,
#         'years_founded': years_founded,
#         'employee_counts': employee_counts,
#         'results': results
#     })


# @login_required
# def manage_users(request):
#     if request.method == 'POST':
#         if 'add_user' in request.POST:
#             username = request.POST.get('username')
#             email = request.POST.get('email')
#             password = request.POST.get('password')  # Get password from form
#             User.objects.create_user(username=username, email=email, password=password)  # Include password
#         elif 'delete_user' in request.POST:
#             user_id = request.POST.get('user_id')
#             User.objects.filter(id=user_id).delete()

#     users = User.objects.all()
#     return render(request, 'manage_users.html', {'users': users})




@login_required
@api_view(['GET'])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


def check_insertion_progress(request, cache_key):
    progress = cache.get(cache_key, 0)  # Default to 0 if not set
    return JsonResponse({'progress': progress})


def async_process_csv(file_path, cache_key, user):
    # Define the mapping between CSV headers and model field names
    header_mapping = {
        ' ': 'revenue',  # Handle cases where the header is just a space
        'year founded': 'year_founded',
        'size range': 'size_range',
        'linkedin url': 'linkedin_url',
        'current employee estimate': 'current_employee_estimate',
        'total employee estimate': 'total_employee_estimate',
        # Add more mappings if necessary
    }

    try:
        print(f"Processing file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            # If the file is tab-delimited, set the delimiter to '\t'
            reader = csv.DictReader(f)   # Specify tab as the delimiter

            companies = []
            total_rows = sum(1 for _ in reader)
            f.seek(0)  # Reset reader after counting rows
            next(reader)  # Skip the header

            # Increase batch size to optimize bulk inserts
            batch_size = 20000  # Try higher batch sizes
            with transaction.atomic():  # Wrap everything in a transaction for efficiency
                for i, row in enumerate(reader):
                    # Create a new dictionary to map the CSV headers to the model fields
                    company_data = {}

                    # Map headers from CSV to the correct model field names
                    for csv_header, value in row.items():
                        csv_header = csv_header.strip()  # Strip any extra whitespace from headers
                        if csv_header == '':  # Check for empty header and map to 'revenue'
                            csv_header = 'revenue'
                        # If the header has a mapped value, use it; otherwise, use the header as is
                        model_field = header_mapping.get(csv_header, csv_header)
                        company_data[model_field] = value.strip() if isinstance(value, str) else value  # Strip values

                    # Handle 'year_founded' specifically to ensure it's an integer
                    year_founded = company_data.get('year_founded', None)
                    if year_founded:
                        try:
                            year_founded = int(float(year_founded))  # Convert to integer
                        except ValueError:
                            year_founded = None
                    else:
                        year_founded = None
                    company_data['year_founded'] = year_founded

                    # Handle employee estimates to ensure they are integers
                    current_employee_estimate = company_data.get('current_employee_estimate', None)
                    if not current_employee_estimate or not current_employee_estimate.strip().isdigit():
                        current_employee_estimate = None
                    company_data['current_employee_estimate'] = current_employee_estimate

                    total_employee_estimate = company_data.get('total_employee_estimate', None)
                    if not total_employee_estimate or not total_employee_estimate.strip().isdigit():
                        total_employee_estimate = None
                    company_data['total_employee_estimate'] = total_employee_estimate

                    # Add the user manually, as it's missing from the CSV
                    company_data['user'] = user

                    # Ensure all keys in company_data are strings before passing to Company(**company_data)
                    company_data = {str(k): v for k, v in company_data.items()}

                    # Create a Company object and append it to the list
                    company = Company(**company_data)
                    companies.append(company)

                    # Insert in batches to optimize performance
                    if len(companies) >= batch_size:
                        Company.objects.bulk_create(companies, ignore_conflicts=True)
                        companies.clear()

                    # Update progress in cache
                    cache.set(cache_key, (i + 1) / total_rows * 100)

                # Insert any remaining companies
                if companies:
                    Company.objects.bulk_create(companies, ignore_conflicts=True)

        # Remove the file after processing
        os.remove(file_path)

        # Mark as complete
        cache.set(cache_key, 100)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error occurred during CSV processing: {e}")
        cache.set(cache_key, -1)  # Mark as failed

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

            # Save the file temporarily
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Generate a cache key for tracking progress
            cache_key = f'csv_progress_{request.user.id}_{filename}'

            # Start processing CSV in a separate thread to avoid blocking
            thread = threading.Thread(target=async_process_csv, args=(file_path, cache_key, request.user))
            thread.start()

            return JsonResponse({'cache_key': cache_key})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def query_builder(request):
    # Query distinct values from the database and order them systematically
    industries = Company.objects.filter(user=request.user).values_list('industry', flat=True).distinct().order_by('industry')
    size_ranges = Company.objects.filter(user=request.user).values_list('size_range', flat=True).distinct()
    states = Company.objects.filter(user=request.user).values_list('locality', flat=True).distinct().order_by('locality')
    countries = Company.objects.filter(user=request.user).values_list('country', flat=True).distinct().order_by('country')
    years_founded = Company.objects.filter(user=request.user).values_list('year_founded', flat=True).distinct().order_by('year_founded')

    # Create a list of employee ranges with 'from' and 'to' values
    employee_counts = [
        {'from': 1, 'to': 100},
        {'from': 101, 'to': 200},
        {'from': 201, 'to': 500},
        {'from': 501, 'to': 1000},
        {'from': 1001, 'to': 5000},
        {'from': 5001, 'to': 10000},
        {'from': 10001, 'to': 50000},
        {'from': 50001, 'to': None},  # No upper bound for this range
    ]

    form = QueryForm(request.GET or None)
    query = Company.objects.filter(user=request.user).only('name', 'industry', 'current_employee_estimate', 'locality', 'size_range', 'country')

    # Filter parameters
    industry = request.GET.get('industry')
    size_range = request.GET.get('size_range')
    state = request.GET.get('state')
    employees_from = request.GET.get('employees_from')
    country = request.GET.get('country')
    year_founded = request.GET.get('year_founded')

    # Apply filters to the query
    if industry:
        query = query.filter(industry__icontains=industry)
    if size_range:
        query = query.filter(size_range__icontains=size_range)
    if state:
        query = query.filter(locality__icontains=state)  # Changed from 'address__icontains' to 'locality__icontains'
    if employees_from:
        query = query.filter(current_employee_estimate__gte=employees_from)
    if country:
        query = query.filter(country__icontains=country)
    if year_founded:
        query = query.filter(year_founded__icontains=year_founded)

    results = query.count()

    return render(request, 'query.html', {
        'form': form,
        'industries': industries,
        'size_ranges': size_ranges,
        'states': states,
        'countries': countries,
        'years_founded': years_founded,
        'employee_counts': employee_counts,
        'results': results
    })


@login_required
def manage_users(request):
    if request.method == 'POST':
        if 'add_user' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')  # Get password from form
            User.objects.create_user(username=username, email=email, password=password)  # Include password
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            User.objects.filter(id=user_id).delete()

    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})
