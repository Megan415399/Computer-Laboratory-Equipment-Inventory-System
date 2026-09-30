from django.shortcuts import render, redirect
from .models import Equipment


def index(request):
    return render(request, 'equipment/index.html')


def equipment_list(request):
    equipments = Equipment.objects.all()

    context = {
        'equipments': equipments
    }

    return render(request, 'equipment/equipment_list.html', context)


def equipment_create(request):
    if request.method == 'POST':
        Equipment.objects.create(
            equipment_name=request.POST['equipment_name'],
            category=request.POST['category'],
            brand=request.POST['brand'],
            quantity=request.POST['quantity'],
            condition=request.POST['condition'],
            status=request.POST['status'],
            location=request.POST['location']
        )

        return redirect('equipment_list')

    return render(request, 'equipment/equipment_form.html')

def equipment_update(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)

    if request.method == 'POST':
        equipment.equipment_name = request.POST['equipment_name']
        equipment.category = request.POST['category']
        equipment.brand = request.POST['brand']
        equipment.quantity = request.POST['quantity']
        equipment.condition = request.POST['condition']
        equipment.status = request.POST['status']
        equipment.location = request.POST['location']

        equipment.save()

        return redirect('equipment_list')

    context = {
        'equipment': equipment
    }

    return render(request, 'equipment/equipment_form.html', context)

def equipment_delete(request, equipment_id):
    equipment = Equipment.objects.get(equipment_id=equipment_id)

    if request.method == 'POST':
        equipment.delete()
        return redirect('equipment_list')

    context = {
        'equipment': equipment
    }

    return render(request, 'equipment/equipment_confirm_delete.html', context)