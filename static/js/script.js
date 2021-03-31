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

$('.bi-sliders').on('click', function() {
    $('.extend').css('display', 'block');
    $('label[for=search-field]').css('display', 'inline');
    $(this).css('opacity', 0);
    $('#search-field').attr('required', 'required');
    $('.button-search').css('margin-left', '1.3rem');
    $('#city').attr('required', 'required');
    $('#sex').attr('required', 'required');
    $('#salary').attr('required', 'required');
    $('#from_date').attr('required', 'required');
    $('#till_date').attr('required', 'required');
})