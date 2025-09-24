from .models import Customer, Order, OrderItem, Product
from decimal import Decimal
from django.db.models import Q, F

# crud basics - create


def addCustomer(name: str, email: str):

    newCustomer = Customer.objects.create(name=name, email=email)
    print(newCustomer)


def getCustomerList():

    customers = Customer.objects.all()
    result = dict()
    result['total'] = customers.count()
    result['list'] = customers

    print(result)


def getCustomer(id: int):

    customer = Customer.objects.get(id=id)
    print(customer)
    return customer


def addProduct(name: str, price: Decimal, stock: int):

    result = Product.objects.create(
        name=name, price=price, stock=stock)
    print(result)


def getProductList():

    products = Product.objects.all()
    result = dict(total=products.count(), list=list)

    print(result)
    return result


def getProduct(productId: int):

    product = Product.objects.get(id=productId)
    print(product)
    return product


def updateProductPrice(productId: int, price: Decimal):

    product = getProduct(productId)

    product.price = price
    product.save()

    print(product)
    return product


def decreaseProductStock(productId: int):
    try:
        product = getProduct(productId)
        if product.stock > 0:
            product.stock -= 1
            product.save()
            print(f"Stock decreased. New stock: {product.stock}")
            return product
        else:
            print(f"Product with id {productId} is out of stock.")
            return None
    except Product.DoesNotExist:
        print(f"Product with id {productId} does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def addOrder(customerId: int):

    customer = getCustomer(customerId)

    result = Order.objects.create(customer=customer)

    print(result)
    return (result)


def getOrderList():

    orders = Order.objects.all()
    result = dict(total=orders.count(), orders=orders)
    print(result)

    return result


def getOrder(orderId: int):

    order = Order.objects.get(id=orderId)
    print(order)
    return order


def deleteOrder(orderId: int):

    try:
        order = getOrder(orderId=orderId)
        order.delete()
        print('deleted')
        return True
    except Order.DoesNotExist:
        print(f'Order with Id {orderId} Not Found')
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def addOrderItem(ordeId: int, productId: int, quantity: int):

    order = getOrder(orderId=ordeId)
    product = getProduct(productId=productId)

    result = OrderItem.objects.create(
        order=order, product=product, quantity=quantity)
    print(result)
    return result


# Filters & Lookups
def getProductsCheaperThan(price: Decimal):

    products = Product.objects.filter(price__lt=price)
    result = dict(total=products.count(), products=products)
    print(result)
    return result


def searchProductsByName(keyword: str):

    products = Product.objects.filter(name__icontains=keyword)
    result = dict(total=products.count(), products=products)

    print(result)
    return result


def getOrdersByYear(year: int):

    orders = Order.objects.filter(created_at__year=year)
    result = dict(total=orders.count(), orders=orders)

    print(result)
    return result


def excludeCustomer(email: str):

    customers = Customer.objects.all().exclude(email=email)
    result = dict(total=customers.count(), customers=customers)

    print(result)
    return result


def getLatestOrder():

    order = Order.objects.all().order_by('created_at').last()
    print(order)
    return order


# Q & F Expressions

def searchProductByNameorPrice(name: str, price: Decimal):

    products = Product.objects.filter(
        Q(name__icontains=name) | Q(price__lt=price))
    result = dict(total=products.count(), products=products)
    print(result)
    return result


def getOrdersByCustomerOrYear(customerId: int, year: int):

    orders = Order.objects.filter(
        Q(customer__id=customerId) | Q(created_at__year=year))
    result = dict(total=orders.count(), orders=orders)
    print(result)
    return result


def compareStockAndQuantity(productId: int, quantity: int):

    product = Product.objects.filter(id=productId, stock__gte=quantity).first()

    print(product)
    return (product)


def discountProductsIfStockLow(threshold: int, discount: Decimal):

    updated_count = Product.objects.filter(
        stock__lt=threshold).update(price=F('price') - discount)
    print(f"Discount applied to {updated_count} products.")
    return updated_count

# Relationships


def getOrdersByCustomer(customerId: int):

    orders = Order.objects.filter(customer__id=customerId)
    result = dict(total=orders.count(), orders=orders)
    print(result)
    return result


def getOrderItems(orderId: int):

    items = OrderItem.objects.filter(order__id=orderId)
    result = dict(total=items.count(), items=items)
    print(result)
    return result


def getCustomerOrderProducts(customerId: int):

    products = Product.objects.filter(
        orderItems__order__customer__id=customerId).distinct()

    result = dict(total=products.count(), products=products)
    print(result)
    return result


def getOrdersWithCustomer():

    orders = Order.objects.select_related('customer').all()
    result = dict(total=orders.count(), orders=orders)
    print(result)
    return result


def getOrdersWithItemsAndProducts():

    orders = Order.objects.prefetch_related('orderItems__product').all()
    result = dict(total=orders.count(), orders=orders)
    print(result)
    return result
