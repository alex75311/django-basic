"use strict";

let _quantity, _price, orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;
let quantityArr = [];
let priceArr = [];
let $orderTotalQuantityDOM;

let totalForms;
let orderTotalQuantity;
let orderTotalCost;
let $orderForm;

function parseOrderForm() {
    for (let i = 0; i < totalForms; i++){
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = _quantity;
        priceArr[i] = (_price) ? _price : 0;
    }
}

function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
    deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost = (Number(orderTotalCost) + deltaCost).toFixed(2);
    orderTotalQuantity = orderTotalQuantity + deltaQuantity;

    $('.order_total_cost').html(orderTotalCost.toString().replace('.', ','));
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;

    orderItemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderItemNum] || 0;
    orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
}

function updateTotalQuantity() {
    for (let i = 0; i < totalForms; i++){
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost).toFixed(2).toString());
}

window.onload = function () {
    $orderTotalQuantityDOM = $('.order_total_quantity');
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text());
    orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    $orderForm = $('.order_form');

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(event.target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderItemNum];
        } else {
            deltaQuantity = quantityArr[orderItemNum];
        }
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
    });

    $orderForm.on('change', 'select', function (event) {
        let product_id = this;
        let product_price = product_id.parentElement.parentElement.children[2];
        let product_quantity = product_id.parentElement.parentElement.children[1].lastElementChild;
        let target_class = event.target.name.replace('-product', '-price');
        let orderItemNum = event.target.name.replace('orderitems-', '').replace('-product', '');

        if (priceArr[orderItemNum] && quantityArr[orderItemNum]) {
            orderSummaryUpdate(
                priceArr[orderItemNum],
                -parseInt(product_quantity.value));
        }
        quantityArr[orderItemNum] = 0;

        $.ajax({
            url: '/ajax/product/' + product_id.value + '/',
            success: function (data) {
                product_price.innerHTML = '<span class=' + target_class + '>' +
                    data['product_price'].replace('.', ',') + '</span>' + '$';
                product_quantity.value = '0';
                priceArr[orderItemNum] = parseFloat(data['product_price']);
                if (isNaN(quantityArr[orderItemNum])) {
                    quantityArr[orderItemNum] = 0;
                }
                orderSummaryUpdate(
                    priceArr[orderItemNum],
                    parseInt(product_quantity.value));
            }
        })
    })

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });
}