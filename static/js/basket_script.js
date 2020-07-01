window.onload = function () {
    $('.cart_inner').on('change', 'input[type="number"]', function (event) {
        let t_href = event.target
        $.ajax({
            url: "/basket/edit/" + t_href.dataset['pk'] + '/' + t_href.value + '/',
            success: function (data) {
                $('.cart_inner').html(data.result);
            },
        });

        event.preventDefault();
    });

    $('.cart_inner').on('click', '#remove', function (event) {
        let remove = event.target
        $.ajax({
            url: "/basket/remove/" + remove.dataset['el'] + "/",
            success: function(data){
                $('.cart_inner').html(data.result)
                console.log(data.result)
            },
        });
    })
}
