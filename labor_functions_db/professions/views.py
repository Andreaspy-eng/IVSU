from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import (
    Profession,
    GeneralizedLaborFunction,
    LaborFunction,
    LaborAction,
    RequiredKnowledge,
    RequiredSkill,
    OKSO
)

def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            
            for index, row in df.iterrows():
                # Проверка уровня квалификации
                if row['Уровень квалификации'] not in [6, 7]:
                    raise ValueError(f"Ошибка в строке {index + 1}: уровень должен быть 6 или 7")
                
                # Создаем или получаем профессию
                profession, _ = Profession.objects.get_or_create(
                    name=row['Название профессии'],
                    defaults={'okpdtr_code': row['Код ОКПДТР']}
                )
                
                # Создаем или получаем обобщенную трудовую функцию (ОТФ)
                generalized_function, _ = GeneralizedLaborFunction.objects.get_or_create(
                    code=row['Код ОТФ'],
                    defaults={'name': row['Трудовая функция']}
                )
                
                # Создаем трудовую функцию
                labor_function = LaborFunction.objects.create(
                    code=row['Код профессии'],
                    name=row['Трудовая функция'],
                    qualification_level=row['Уровень квалификации'],
                    profession=profession,
                    generalized_function=generalized_function
                )
                
                # Добавляем трудовые действия
                if pd.notna(row['Трудовые действия']):
                    actions = [a.strip() for a in str(row['Трудовые действия']).split(';')]
                    for action in actions:
                        LaborAction.objects.create(
                            description=action,
                            labor_function=labor_function
                        )
                
                # Добавляем необходимые знания
                if pd.notna(row['Необходимые знания']):
                    knowledge_list = [k.strip() for k in str(row['Необходимые знания']).split(';')]
                    for knowledge in knowledge_list:
                        RequiredKnowledge.objects.create(
                            description=knowledge,
                            labor_function=labor_function
                        )
                
                # Добавляем необходимые умения
                if pd.notna(row['Необходимые умения']):
                    skills = [s.strip() for s in str(row['Необходимые умения']).split(';')]
                    for skill in skills:
                        RequiredSkill.objects.create(
                            description=skill,
                            labor_function=labor_function
                        )
                
                # Добавляем ОКСО
                OKSO.objects.create(
                    code=row['Код ОКСО'],
                    profession=profession
                )
            
            messages.success(request, 'Данные успешно загружены!')
            return redirect('search')
        
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            return redirect('upload')
    
    return render(request, 'upload.html')

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