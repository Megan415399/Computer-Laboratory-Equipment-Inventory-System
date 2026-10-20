from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Equipment

ITEMS_PER_PAGE = 10

DEFAULT_CATEGORIES = [
    'Input Device',
    'Output Device',
    'Processing Unit',
    'Storage Device',
    'Networking Device',
    'Power Equipment',
    'Accessories',
]


def _parse_quantity(value):
    """Return a whole number >= 0, or None if the value is not valid."""
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        return None
    return quantity if quantity >= 0 else None


def _category_options():
    """Suggested categories: the common ones plus any already used in the database."""
    used = Equipment.objects.values_list('category', flat=True).distinct()
    return sorted(set(DEFAULT_CATEGORIES) | {c for c in used if c})


def index(request):
    context = {
        'total_count': Equipment.objects.count(),
        'available_count': Equipment.objects.filter(status='Available').count(),
        'maintenance_count': Equipment.objects.filter(status='Under Maintenance').count(),
        'damaged_count': Equipment.objects.filter(condition='Damaged').count(),
        'recent_equipment': Equipment.objects.order_by('-equipment_id')[:5],
    }
    return render(request, 'equipment/index.html', context)


def equipment_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    condition = request.GET.get('condition', '')

    equipments = Equipment.objects.all().order_by('equipment_id')

    if query:
        equipments = equipments.filter(
            Q(equipment_name__icontains=query)
            | Q(brand__icontains=query)
            | Q(category__icontains=query)
        )
    if category:
        equipments = equipments.filter(category=category)
    if status:
        equipments = equipments.filter(status=status)
    if condition:
        equipments = equipments.filter(condition=condition)

    paginator = Paginator(equipments, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Keep the search and filters when moving between pages
    params = request.GET.copy()
    params.pop('page', None)

    def distinct(field):
        values = Equipment.objects.order_by(field).values_list(field, flat=True).distinct()
        return [value for value in values if value]

    context = {
        'page_obj': page_obj,
        'total_results': paginator.count,
        'querystring': params.urlencode(),
        'query': query,
        'category': category,
        'status': status,
        'condition': condition,
        'has_filters': any([query, category, status, condition]),
        'categories': distinct('category'),
        'statuses': distinct('status'),
        'conditions': distinct('condition'),
    }

    return render(request, 'equipment/equipment_list.html', context)


def equipment_create(request):
    if request.method == 'POST':
        quantity = _parse_quantity(request.POST.get('quantity'))
        if quantity is None:
            messages.error(request, 'Quantity must be a whole number, 0 or higher.')
            return redirect('equipment_create')

        equipment = Equipment.objects.create(
            equipment_name=request.POST['equipment_name'].strip(),
            category=request.POST['category'].strip(),
            brand=request.POST['brand'].strip(),
            quantity=quantity,
            condition=request.POST['condition'],
            status=request.POST['status'],
            location=request.POST['location'].strip(),
        )

        messages.success(request, f'"{equipment.equipment_name}" was added to the inventory.')
        return redirect('equipment_list')

    return render(request, 'equipment/equipment_form.html', {
        'category_options': _category_options(),
    })


def equipment_update(request, equipment_id):
    equipment = get_object_or_404(Equipment, equipment_id=equipment_id)

    if request.method == 'POST':
        quantity = _parse_quantity(request.POST.get('quantity'))
        if quantity is None:
            messages.error(request, 'Quantity must be a whole number, 0 or higher.')
            return redirect('equipment_update', equipment_id=equipment_id)

        equipment.equipment_name = request.POST['equipment_name'].strip()
        equipment.category = request.POST['category'].strip()
        equipment.brand = request.POST['brand'].strip()
        equipment.quantity = quantity
        equipment.condition = request.POST['condition']
        equipment.status = request.POST['status']
        equipment.location = request.POST['location'].strip()
        equipment.save()

        messages.success(request, f'"{equipment.equipment_name}" was updated.')
        return redirect('equipment_list')

    context = {
        'equipment': equipment,
        'category_options': _category_options(),
    }

    return render(request, 'equipment/equipment_form.html', context)


def equipment_delete(request, equipment_id):
    equipment = get_object_or_404(Equipment, equipment_id=equipment_id)

    if request.method == 'POST':
        name = equipment.equipment_name
        equipment.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect('equipment_list')

    # Fallback page (used only if JavaScript is off)
    context = {
        'equipment': equipment
    }

    return render(request, 'equipment/equipment_confirm_delete.html', context)