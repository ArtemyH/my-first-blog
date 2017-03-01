function plus() {
    var pk = $('.post').data('pk');
    $.get('/post/plus/', {post_pk: pk}, function(data){
        $('#rate_count').html(data);
    });
};

function minus() {
    var pk = $('.post').data('pk');
    $.get('/post/minus/', {post_pk: pk}, function(data){
        $('#rate_count').html(data);
    });
};