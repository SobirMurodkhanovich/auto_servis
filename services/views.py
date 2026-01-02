from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomLoginForm
from .models import AutoMobile, Service, AutoService
from django.db.models import Q
from django.db import models


# Create your views here.
def index_page(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # ROLE bo‘yicha yo‘naltirish
                if hasattr(user, 'role'):
                    if user.role == 'employee':
                        return redirect('employee-page')
                    elif user.role == 'user':
                        return redirect('index-page')
                # Agar role aniqlanmasa, index-page ga yo‘naltirish
                return redirect('index-page')
            else:
                form.add_error(None, "Noto‘g‘ri username yoki parol.")
    else:
        form = CustomLoginForm(request=request)

    return render(request, 'register/login.html', {'form': form})


def employee_view(request):
    return render(request, 'role/employee.html')


def auto_list_view(request):
    query = request.GET.get('q', '')  # Search inputdan keladigan qiymat
    if query:
        autos = AutoMobile.objects.filter(automobile_number__icontains=query).order_by('-created_at')
    else:
        autos = AutoMobile.objects.all().order_by('-created_at')

    context = {
        'autos': autos,
        'query': query,  # input value uchun template ga yuboriladi
    }
    return render(request, 'role/avto_list.html', context)


def auto_add_view(request):
    if request.method == 'POST':
        # POST orqali kelgan ma'lumotlarni olamiz
        customer_name = request.POST.get('customer_name')
        customer_phone_number = request.POST.get('customer_phone_number')
        automobile_number = request.POST.get('automobile_number')
        mileage = request.POST.get('mileage')

        # Barcha maydonlar to'ldirilganligini tekshiramiz
        if customer_name and customer_phone_number and automobile_number and mileage:
            # AutoMobile obyektini yaratamiz va saqlaymiz
            auto = AutoMobile.objects.create(
                customer_name=customer_name,
                customer_phone_number=customer_phone_number,
                automobile_number=automobile_number,
                mileage=mileage
            )
            return redirect('auto-list')  # Shu sahifaga qaytadi

        else:
            pass

    return render(request, 'role/avto_add.html')


def auto_edit_view(request, pk):
    # Avtomobilni olish, agar topilmasa 404
    auto = get_object_or_404(AutoMobile, pk=pk)

    if request.method == 'POST':
        # Formdan kelgan qiymatlarni olish
        customer_name = request.POST.get('customer_name', '').strip()
        customer_phone_number = request.POST.get('customer_phone_number', '').strip()
        automobile_number = request.POST.get('automobile_number', '').strip()
        mileage = request.POST.get('mileage', '').strip()

        # Ma'lumotlarni yangilash
        auto.customer_name = customer_name
        auto.customer_phone_number = customer_phone_number
        auto.automobile_number = automobile_number
        auto.mileage = mileage if mileage.isdigit() else 0  # Agar son bo'lmasa 0 qo'yiladi
        auto.save()

        # Tahrirdan keyin avtomobillar ro'yxatiga qaytish
        return redirect('auto-list')

    # GET request uchun formni oldingi qiymatlar bilan ko'rsatish
    context = {
        'auto': auto
    }
    return render(request, 'role/avto_edit.html', context)


def auto_delete_view(request, pk):
    # Avtomobilni olish, agar topilmasa 404
    auto = get_object_or_404(AutoMobile, pk=pk)

    # O'chirish
    auto.delete()

    # O'chirilgandan keyin avtomobillar ro'yxatiga qaytish
    return redirect('auto-list')


def services_view(request):
    query = request.GET.get('q')  # Search qatorini olish
    if query:
        # Service modelida service_name maydoni bo'yicha filter
        services = Service.objects.filter(
            Q(service_name__icontains=query)  # icontains - katta/kichik harf farqi yo'q
        )
    else:
        services = Service.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'role/services.html', context)


def services_add_view(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        service_price = request.POST.get('service_price')

        # Oddiy validatsiya
        if service_name and service_price:
            Service.objects.create(
                service_name=service_name,
                service_price=service_price
            )
            return redirect('services-page')  # Xizmatlar ro'yxati sahifasiga yo'naltirish
        else:
            # Agar bo'sh maydonlar bo'lsa, xatolik yuborish
            context = {
                'form_errors': True,
            }
            return render(request, 'role/services_add.html', context)

    # GET so'rov bo'lsa, formani bo'sh ko'rsatish
    return render(request, 'role/services_add.html')


def services_edit(request, pk):
    # Ma'lum bir xizmatni olish
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        # Formadan qiymatlarni olish
        service_name = request.POST.get('service_name')
        service_price = request.POST.get('service_price')

        # Qiymatlarni yangilash
        service.service_name = service_name
        service.service_price = service_price
        service.save()  # Bazaga saqlash

        # Saqlangandan keyin xizmatlar ro'yxatiga yo'naltirish
        return redirect('services-page')

    # GET so'rov bo'lsa, formani oldindan to'ldirib ko'rsatish
    context = {
        'service': service
    }
    return render(request, 'role/services_edit.html', context)


def services_delete(request, pk):
    # Ma'lum bir xizmatni olish, agar topilmasa 404
    service = get_object_or_404(Service, pk=pk)

    # Xizmatni o'chirish
    service.delete()

    # O'chirishdan keyin xizmatlar ro'yxatiga yo'naltirish
    return redirect('services-page')



def auto_service_page(request):
    # Barcha avtomobillar va xizmatlar
    # Oxirgi qo‘shilgan avtomobillar birinchi bo‘lsin
    autos = AutoMobile.objects.all().order_by('-created_at')
    services = Service.objects.all()

    selected_auto_id = request.GET.get('auto')  # agar avtomobil tanlangan bo'lsa
    selected_auto = None
    auto_service = None

    if selected_auto_id:
        selected_auto = get_object_or_404(AutoMobile, pk=selected_auto_id)
        auto_service, created = AutoService.objects.get_or_create(automobile=selected_auto)

    if request.method == 'POST':
        auto_id = request.POST.get('automobile')
        service_ids = request.POST.getlist('services')  # bir nechta xizmat tanlanadi

        if auto_id and service_ids:
            automobile = get_object_or_404(AutoMobile, pk=auto_id)
            auto_service, created = AutoService.objects.get_or_create(automobile=automobile)

            # Xizmatlarni biriktirish
            auto_service.services.set(service_ids)

            # ===== TOTAL SUM HISOBLASH =====
            total = Service.objects.filter(id__in=service_ids).aggregate(
                total=models.Sum('service_price')
            )['total'] or 0

            auto_service.total_sum = total
            auto_service.save()  # DB-ga yozish

            # PDF yaratish front-endda JS orqali bo'ladi
            return redirect('car-services-page')  # POSTdan so'ng redirect

    context = {
        'autos': autos,                # bu yerda eng so'nggi avtomobillar birinchi
        'services': services,
        'selected_auto': selected_auto,
        'auto_service': auto_service,
    }

    return render(request, 'role/car_services.html', context)


def history_view(request):
    query = request.GET.get('q', '').strip()  # qidiruv inputidan so'z

    if query:
        autoservices = AutoService.objects.filter(
            Q(automobile__automobile_number__icontains=query)
        ).order_by('-created_at')
    else:
        autoservices = AutoService.objects.all().order_by('-created_at')

    context = {
        'autoservices': autoservices,
        'query': query,
    }
    return render(request, 'role/history.html', context)


def history_detail_view(request, pk):
    # AutoService obyektini olish
    auto_service = get_object_or_404(AutoService, automobile_id=pk)

    # Ushbu avtomobilga biriktirilgan xizmatlar
    services = auto_service.services.all()

    # Jami summa
    total = services.aggregate(total=models.Sum('service_price'))['total'] or 0

    context = {
        'auto': auto_service.automobile,
        'services': services,
        'total': total,
    }

    return render(request, 'role/history_detail.html', context)
