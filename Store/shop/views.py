from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import OrderForm

# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('frontpage')


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render (request, 'shop/search.html',{
        'query': query,
        'products': products,
    })


def category_detail(request,slug):
    category=get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'shop/category_detail.html', {
                      'category':category,
                      'products':products,
                  })

def product_detail(request,category_slug, slug):
    product=get_object_or_404(Product, slug=slug, status=Product.ACTIVE)

    return render(request, 'shop/product_detail.html', {
        'product':product
    })


def cart_view(request):
    cart = Cart(request)

    return render(request,'shop/cart_view.html', {
        'cart': cart
    })


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)  

        if form.is_valid():
            total_price = 0

            for item in cart:
                product= item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.total_cost = total_price
            order.save()

            for item in cart:
                product= item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price = price, quantity=quantity)

            cart.clear()
            return redirect('myaccount')
        
    else:
        form = OrderForm()

    return render(request,'shop/checkout.html', {
        'cart': cart,
        'form': form,
    })

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')


def change_quantity(request,product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity= -1

        cart = Cart(request)
        cart.add(product_id,quantity, True)

    return redirect('cart_view')

