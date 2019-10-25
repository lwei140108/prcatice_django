let num_show = $('.num_show');

$('.add').click(function () {
    num_show.val(function (i, v) {
        return parseInt(v) + 1
    });
    $('#add_cart').attr('href', '/add_to_cart/' + '?goods_id=' + num_show.attr('data-id') + '&number=' + num_show.val());
});
$('.minus').click(function () {
    num_show.val(function (i, v) {
        if (v > 1) {
            return parseInt(v) - 1
        }
        return v
    });
    $('#add_cart').attr('href', '/add_to_cart/' + '?goods_id=' + num_show.attr('data-id') + '&number=' + num_show.val());
});
num_show.on('input', function () {
    if (!/^\d+$/.test($(this).val())) {
        $(this).val(1)
    }
    $('#add_cart').attr('href', '/add_to_cart/' + '?goods_id=' + num_show.attr('data-id') + '&number=' + num_show.val());
});
