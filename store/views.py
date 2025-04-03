# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Product, Cart, CartItem, DeliveryInfo
from .forms import DeliveryForm



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})



def checkout_view(request):
    # إذا لم يكن المستخدم مسجلاً، يتم توجيهه إلى صفحة التسجيل مع تمرير معامل next
    if not request.user.is_authenticated:
        signup_url = f"{reverse('signup')}?next={reverse('checkout')}"
        return redirect(signup_url)
        
    # إذا كان مسجلاً، يتم عرض نموذج بيانات التوصيل
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            # بعد حفظ بيانات التوصيل، يعود المستخدم إلى صفحة السلة
            return redirect('cart')
    else:
        form = DeliveryForm()
    return render(request, 'store/delivery.html', {'form': form})




def signup_view(request):
    next_page = request.GET.get('next', '')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.POST.get('next', reverse('product_list'))
            return redirect(next_url)
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form, 'next': next_page})

@login_required
def checkout_view(request):
    # إذا لم يكن المستخدم مسجلاً، يتم توجيهه إلى صفحة التسجيل مع معامل next
    if not request.user.is_authenticated:
        signup_url = f"{reverse('signup')}?next={reverse('checkout')}"
        return redirect(signup_url)
        
    # إذا كان مسجلاً، يتم عرض نموذج بيانات التوصيل
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            # بعد حفظ بيانات التوصيل، نقوم بإعادة التوجيه إلى صفحة الفاتورة
            return redirect('invoice')
    else:
        form = DeliveryForm()
    return render(request, 'store/delivery.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    # بعد الإضافة نعيد المستخدم إلى صفحة عرض المنتجات ليرى التحديث
    return redirect('product_list')


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price_after_tax * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request, product_id, action):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def invoice_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price_after_tax * item.quantity for item in cart_items)
    # نحصل على آخر بيانات توصيل للمستخدم (يمكن تعديلها بحسب منطق المشروع)
    delivery_info = DeliveryInfo.objects.filter(user=request.user).last()
    return render(request, 'store/invoice.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'delivery_info': delivery_info
    })


def BOOM (request):
    return render(request, 'store/me.html')
    