$('.add_favorite').on('submit', function(e) {
    var action = $(this).attr('action');
    $.ajax({
        url: action,
        method: 'POST',
        data: $(this).serialize(),
        success: function() {
            if($('.add-favorite svg').css('fill') != 'blue') {
                $('.add-favorite svg').css('fill', 'blue');
                console.log('work');
            }
        }
    })
    e.preventDefault();
});

$('.favorite').on('submit', function(e) {
    var action = $(this).attr('action');
    var star = $('.add-favorite svg');
    $.ajax({
        url: action,
        method: 'POST',
        data: $(this).serialize(),
        success: function(data) {
            console.log('work');
        }
    })
    e.preventDefault();
});

$('.add-favorite').on('click', function() {
    if($(this).find('svg').css('fill') != 'blue') {
        $(this).find('svg').css('fill', 'blue');
    }
})