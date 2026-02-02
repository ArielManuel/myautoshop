from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product   

def home(request):
    featured_products = Product.objects.all()[:3]  
    return render(request, "blog/home.html", {
        "featured_products": featured_products
    })

def about(request):
    return render(request, "blog/about.html")

def services(request):
    return render(request, "blog/services.html")

def contact(request):
    return render(request, "blog/contact.html")
def products(request):
    category = request.GET.get("category")

    if category:
        products = Product.objects.filter(category__iexact=category)
    else:
        products = Product.objects.all()

    return render(request, "blog/products.html", {
        "products": products,
        "active_category": category
    })

# ===== CART (session-based) =====
def _get_cart(request):
    return request.session.get("cart", {})

def cart(request):
    cart_data = _get_cart(request)
    items = []
    total = 0
    to_remove = []

    for pid_str, data in cart_data.items():
        try:
            p = Product.objects.get(id=int(pid_str))
        except Product.DoesNotExist:
            to_remove.append(pid_str)
            continue

        qty = int(data.get("qty", 1))
        subtotal = float(p.price) * qty
        total += subtotal
        items.append({"product": p, "qty": qty, "subtotal": subtotal})

    # linisin yung invalid products sa cart session
    for pid_str in to_remove:
        cart_data.pop(pid_str, None)

    if to_remove:
        request.session["cart"] = cart_data
        request.session.modified = True

    return render(request, "blog/cart.html", {"items": items, "total": total})

def cart_add(request, product_id):
    # ensure product exists
    get_object_or_404(Product, id=product_id)

    cart_data = _get_cart(request)
    pid = str(product_id)

    if pid in cart_data:
        cart_data[pid]["qty"] += 1
    else:
        cart_data[pid] = {"qty": 1}

    request.session["cart"] = cart_data
    request.session.modified = True
    return redirect("cart")


def cart_remove(request, product_id):
    cart_data = _get_cart(request)
    pid = str(product_id)

    if pid in cart_data:
        del cart_data[pid]
        request.session["cart"] = cart_data
        request.session.modified = True

    return redirect("cart")

@require_POST
def cart_update(request, product_id):
    cart_data = _get_cart(request)
    pid = str(product_id)

    try:
        qty = int(request.POST.get("qty", 1))
    except (TypeError, ValueError):
        qty = 1

    if qty <= 0:
        cart_data.pop(pid, None)
    else:
        cart_data[pid] = {"qty": qty}

    request.session["cart"] = cart_data
    request.session.modified = True
    return redirect("cart")
