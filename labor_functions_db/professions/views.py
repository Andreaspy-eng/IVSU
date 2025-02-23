from django.shortcuts import render
from .models import Profession, LaborFunction

def search(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    professions = Profession.objects.filter(name__icontains=query)
    
    if level:
        professions = professions.filter(laborfunction__qualification_level=level).distinct()
    
    return render(request, 'search.html', {'professions': professions})

def profession_detail(request, profession_id):
    profession = Profession.objects.get(id=profession_id)
    labor_functions = LaborFunction.objects.filter(profession=profession)
    return render(request, 'profession_detail.html', {'profession': profession, 'labor_functions': labor_functions})