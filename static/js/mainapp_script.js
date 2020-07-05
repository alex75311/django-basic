window.onload = function () {
    $('.filter-list').on('change', 'input[type="radio"]', function (event) {
        $.ajax({
            url: '/category/' + event.target.id,
            success: function (data){
                $('#products').html(data.result)
            }
        })
    })
}