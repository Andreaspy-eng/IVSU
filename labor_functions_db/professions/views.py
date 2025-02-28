from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.forms import inlineformset_factory
from .forms import ProfessionForm, LaborFunctionForm, GeneralizedLaborFunctionForm, OKSOForm
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

def index(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    
    professions = Profession.objects.all()
    
    # Фильтрация по названию или коду профессии
    if query:
        professions = professions.filter(
            Q(name__icontains=query) | 
            Q(code__icontains=query)
        )
    
    # Фильтрация через связанную модель LaborFunction
    if level:
        professions = professions.filter(
            laborfunction__qualification_level=int(level)
        ).distinct()
    
    # Обработка AJAX-запросов
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('professions/_profession_cards.html', {'professions': professions})
        return HttpResponse(html)
    
    return render(request, 'professions/index.html', {'professions': professions})
    
    return render(request, 'professions/index.html', {'professions': professions})


def add_details(request, profession_id):
    profession = get_object_or_404(Profession, id=profession_id)
    if request.method == 'POST':
        labor_function = LaborFunction.objects.get(profession=profession)
        
        # Трудовые действия
        actions = request.POST.get('actions', '').split(';')
        for action in actions:
            if action.strip():
                LaborAction.objects.create(
                    description=action.strip(),
                    labor_function=labor_function
                )
        
        # Необходимые знания
        knowledge = request.POST.get('knowledge', '').split(';')
        for know in knowledge:
            if know.strip():
                RequiredKnowledge.objects.create(
                    description=know.strip(),
                    labor_function=labor_function
                )
        
        # Необходимые умения
        skills = request.POST.get('skills', '').split(';')
        for skill in skills:
            if skill.strip():
                RequiredSkill.objects.create(
                    description=skill.strip(),
                    labor_function=labor_function
                )
        
        messages.success(request, 'Данные добавлены!')
        return redirect('profession_detail', profession_id=profession.id)
    
    return redirect('profession_detail', profession_id=profession.id)

def add_profession(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        # qualification_level = int(request.POST.get('qualification_level')) 
        okpdtr_code = request.POST.get('okpdtr_code')
        
        try:
            Profession.objects.create(
                name=name,
                code=code,
                okpdtr_code=okpdtr_code
            )
            messages.success(request, 'Профессия успешно добавлена!')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
        
        return redirect('index')
    
    return redirect('index')

def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            
            for _, row in df.iterrows():
                # Проверка обязательных полей
                required_fields = ['Код профессии', 'Название профессии', 'Код ОКПДТР', 
                                  'Трудовая функция', 'Уровень квалификации', 
                                  'Код ОТФ', 'Код ОКСО']
                for field in required_fields:
                    if pd.isna(row[field]):
                        raise ValueError(f"Отсутствует обязательное поле: {field}")

                # Обновление или создание профессии
                profession, created = Profession.objects.update_or_create(
                    code=row['Код профессии'],
                    defaults={
                        'name': row['Название профессии'],
                        'okpdtr_code': row['Код ОКПДТР']
                    }
                )

                # Удаление старых данных, если профессия уже существовала
                if not created:
                    LaborFunction.objects.filter(profession=profession).delete()

                # Создание/обновление Обобщенной трудовой функции (ОТФ)
                generalized_function, _ = GeneralizedLaborFunction.objects.update_or_create(
                    code=row['Код ОТФ'],
                    defaults={'name': row['Трудовая функция']}
                )

                # Создание трудовой функции
                labor_function = LaborFunction.objects.create(
                    name=row['Трудовая функция'],
                    qualification_level=int(row['Уровень квалификации']),
                    profession=profession,
                    generalized_function=generalized_function
                )

                # Добавление ОКСО
                OKSO.objects.update_or_create(
                    code=row['Код ОКСО'],
                    defaults={'labor_function': labor_function}
                )

                # Обработка трудовых действий
                if pd.notna(row.get('Трудовые действия', '')):
                    actions = [a.strip() for a in str(row['Трудовые действия']).split(';') if a.strip()]
                    for action in actions:
                        LaborAction.objects.create(
                            description=action,
                            labor_function=labor_function
                        )

                # Обработка необходимых знаний
                if pd.notna(row.get('Необходимые знания', '')):
                    knowledge_list = [k.strip() for k in str(row['Необходимые знания']).split(';') if k.strip()]
                    for knowledge in knowledge_list:
                        RequiredKnowledge.objects.create(
                            description=knowledge,
                            labor_function=labor_function
                        )

                # Обработка необходимых умений
                if pd.notna(row.get('Необходимые умения', '')):
                    skills = [s.strip() for s in str(row['Необходимые умения']).split(';') if s.strip()]
                    for skill in skills:
                        RequiredSkill.objects.create(
                            description=skill,
                            labor_function=labor_function
                        )

            messages.success(request, 'Данные успешно загружены!')
            
        except Exception as e:
            error_message = f"Ошибка при обработке файла: {str(e)}"
            messages.error(request, error_message)
            print(error_message)  

        return redirect('index')
    
    messages.error(request, 'Файл не выбран!')
    return redirect('index')

def search(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    professions = Profession.objects.filter(name__icontains=query)
    
    if level:
        professions = professions.filter(laborfunction__qualification_level=level).distinct()
    
    return render(request, 'search.html', {'professions': professions})

def profession_detail(request, profession_id):
    profession = get_object_or_404(Profession, id=profession_id)
    labor_functions = LaborFunction.objects.filter(profession=profession)
    
    # Инициализация форм для модального окна
    LaborFunctionFormSet = inlineformset_factory(
        Profession,
        LaborFunction,
        form=LaborFunctionForm,
        extra=1,
        can_delete=True
    )
    
    if request.method == 'POST':
        form = ProfessionForm(request.POST, instance=profession)
        formset = LaborFunctionFormSet(request.POST, instance=profession)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('profession_detail', profession_id=profession.id)
    else:
        form = ProfessionForm(instance=profession)
        formset = LaborFunctionFormSet(instance=profession)

    return render(request, 'profession_detail.html', {
        'profession': profession,
        'labor_functions': labor_functions,
        'profession_form': form,
        'labor_function_formset': formset
    })

def edit_profession(request, profession_id):
    profession = get_object_or_404(Profession, id=profession_id)
    LaborFunctionFormSet = inlineformset_factory(
        Profession, 
        LaborFunction, 
        fields=('name', 'qualification_level'), 
        extra=1
    )

    if request.method == 'POST':
        form = ProfessionForm(request.POST, instance=profession)
        formset = LaborFunctionFormSet(request.POST, instance=profession)
        
        if form.is_valid() and formset.is_valid():
            profession = form.save()
            
            formset.save()
            save_related_data(profession, request.POST)
            
            return redirect('profession_detail', profession_id=profession.id)

    else:
        form = ProfessionForm(instance=profession)
        formset = LaborFunctionFormSet(instance=profession)
    
    # Получаем связанные данные
    labor_actions = LaborAction.objects.filter(labor_function__profession=profession)
    required_knowledge = RequiredKnowledge.objects.filter(labor_function__profession=profession)
    required_skills = RequiredSkill.objects.filter(labor_function__profession=profession)

    return render(request, 'profession_detail.html', {
        'profession': profession,
        'profession_form': form,
        'lf_formset': formset,
        'labor_actions': labor_actions,
        'required_knowledge': required_knowledge,
        'required_skills': required_skills
    })

def save_related_data(profession, post_data):
    # Удаляем старые записи
    LaborAction.objects.filter(labor_function__profession=profession).delete()
    RequiredKnowledge.objects.filter(labor_function__profession=profession).delete()
    RequiredSkill.objects.filter(labor_function__profession=profession).delete()

    # Создаем новые записи
    for lf in profession.laborfunction_set.all():
        # Трудовые действия
        for action in post_data.getlist('actions'):
            if action.strip():
                LaborAction.objects.create(
                    description=action.strip(),
                    labor_function=lf
                )
        
        # Необходимые знания
        for knowledge in post_data.getlist('knowledge'):
            if knowledge.strip():
                RequiredKnowledge.objects.create(
                    description=knowledge.strip(),
                    labor_function=lf
                )
        
        # Необходимые умения
        for skill in post_data.getlist('skills'):
            if skill.strip():
                RequiredSkill.objects.create(
                    description=skill.strip(),
                    labor_function=lf
                )

def delete_profession(request, profession_id):
    profession = get_object_or_404(Profession, id=profession_id)
    profession.delete()
    messages.success(request, 'Профессия удалена!')
    return redirect('index')

def edit_labor_function(request, labor_function_id):
    labor_function = get_object_or_404(LaborFunction, id=labor_function_id)
    
    OKSOFormSet = inlineformset_factory(
        LaborFunction,
        OKSO,
        form=OKSOForm,
        extra=1
    )
    
    if request.method == 'POST':
        form = LaborFunctionForm(request.POST, instance=labor_function)
        okso_formset = OKSOFormSet(request.POST, instance=labor_function)
        
        if form.is_valid() and okso_formset.is_valid():
            form.save()
            okso_formset.save()
            return redirect('edit_profession', profession_id=labor_function.profession.id)
    
    else:
        form = LaborFunctionForm(instance=labor_function)
        okso_formset = OKSOFormSet(instance=labor_function)
    
    return render(request, 'professions/edit_labor_function.html', {
        'form': form,
        'okso_formset': okso_formset,
        'labor_function': labor_function
    })