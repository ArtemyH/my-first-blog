function plus() {
                $.get('/post/plus/', {post_pk: pk}, function(data){
                    $('#rate_count').html(data);
            });
};

function minus() {
                $.get('/post/minus/', {post_pk: pk}, function(data){
                    $('#rate_count').html(data);
            });
};