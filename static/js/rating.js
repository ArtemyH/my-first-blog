<script>
       $('#plus').click(function(){
            $.get('/post/plus/', {post_pk: {{ post.pk }}}, function(data){
                $('#rate_count').html(data);
        });

    });
        
        $('#minus').click(function(){
            $.get('/post/minus/', {post_pk: {{ post.pk }}}, function(data){
                $('#rate_count').html(data);
        });

    });
</script>