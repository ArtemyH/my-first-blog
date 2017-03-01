function sort(cat){
        var field = $("#field").val();
        var order = $("#order").val();
        var category = cat;
        if (cat == undefined){
            var category = window.location.href;
            //alert('cat ' + window.location.href);
        }
        
      $.get('/sort/', {field: field, order: order, category: category}, function(data){
          var json_data = JSON.parse(data)
          
          var formatter = new Intl.DateTimeFormat("en", {
              year: "numeric",
              month: "short",
              day: "numeric",
              hour: "numeric",
              minute: "numeric",
              hour12: "true"
            });
          
          
          $('.my_posts').empty();
          
          $.each(json_data, function(key, value){
              
              $('.my_posts').append('<div class="post"> <div class="date">' + formatter.format(Date.parse(value['published_date'])) + '</div>' +
                                    '<h1><a href="post/' + value['pk'] + '/">' + value['title'] + '</a></h1>' +
                                    '<p>' + value['description'] + '</p>' +
                                    '<p>Автор: <a href="users_list/profile/' + value['author'] + '/">' + value['author__username'] + '</a></p>' +
                                    '</div>');
              });
          }, "json"
           )
    };
    

    function set_active_nav_link(){
        $('.nav-link').each(function(){
            //alert($(this).attr('href') + '  ==  ' + window.location.href);
               if ('http://127.0.0.1:8000/'+$(this).attr('href') == window.location.href){                    
                   $(this).parent().addClass('active'); 
               } else {
                   $(this).parent().removeClass('active');
               };
           });        
    };

    $(document).ready(sort());
    $(document).ready(set_active_nav_link());

    $(document).ready(function(){
        
        
       $('.nav-link').click(function(){
           $('.nav-link').each(function(){
               $(this).parent().removeClass('active');
           });                  
           
           $('.data-category').data['cat'] = this;
           $(this).parent().addClass('active');
           sort(this.href);
       });
    });
    
    