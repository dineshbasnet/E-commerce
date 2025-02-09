from django.shortcuts import render, redirect
from .models import Product, Category, Brand
from django.db.models import Prefetch
from django.db.models import Count, Max, Min
from django.core.paginator import Paginator


def product_detail_view(request, product_id):
    
    try:
        product = Product.objects.prefetch_related(
                    'images', 
                    'categories'
                    ).select_related(
                    'brand'
                    ).get(id=product_id)
    except Product.DoesNotExist:
        return redirect('shop_view')
    except Exception as e:
        print(e)
        return redirect('shop_view')
    else:
        context = {
            'product': product
        }

    
    return render(request, 'shop/product_detail.html', context)


def brand_view(request, brand_id):
    request.session['brand_id'] = brand_id
    return redirect('shop_view')


def category_brand_view(request, category_id, brand_id):
    request.session['category_id'] = category_id
    request.session['brand_id'] = brand_id
    return redirect('shop_view')
    
    


def shop_view(request):    
     
    products = Product.objects.prefetch_related('images').all()
       
    brand_id = request.session.get('brand_id', None)
    category_id = request.session.get('category_id', None)
    vendor_id = request.session.get('vendor_id',None)
    
    # if category id and brand id is given filter products by category and brand
    if category_id:
        category_id = category_id
        request.session['category_id'] = None
        products = products.filter(
            categories__id__contains=category_id
            ).prefetch_related('images').all()
    
    if brand_id:
        brand_id = brand_id
        request.session['brand_id'] = None
        products = products.filter(
            brand_id=brand_id,
           
            ).prefetch_related('images').all()
        
    if vendor_id:
        vendor_id = vendor_id
        request.session['vendor_id']=None
        products = products.filter(
            vendor_id=vendor_id
        ).prefetch_related('images').all
        



        
        
    try:
        filter_min_price, filter_max_price = [float(price) for price in request.GET.get('price-range').split(',')]
    except:
        pass
    else:
        products = products.filter(price__range=(filter_min_price, filter_max_price)).prefetch_related('images').all()
        
    # fetch all categories
    categories = Category.objects.prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.select_related('brand'),
            to_attr='prefetched_products'
        )
    )
    
    # add brands data to each category
    categories_with_brands = {}
    for category in categories:
        brands = {product.brand for product in category.prefetched_products 
                  if product.brand }
        if category.name not in categories_with_brands:
            categories_with_brands[category.name] = {
                'category_id': category.id,
                'brands':list(brands)
            }
        else:
            categories_with_brands[category.name].extend(
                {
                    'category_id': category.id,
                    'brands':list(brands)
                }
            )
    



    brands_with_product_count = Brand.objects.annotate(
        total_products = Count('products')
    )


    prices = Product.objects.aggregate(
        min_price = Min('price'),
        max_price = Max('price')
    )    
    

    page = request.GET.get('page', 1)
    paginated_products = Paginator(products, 8)
    context = {
        'products': paginated_products.page(page),
        'categories': categories_with_brands,
        'brands': brands_with_product_count,
        'min_price': prices['min_price'],
        'max_price': prices['max_price'],
        
    }
    
    return render(request, 'shop/shop.html', context)