function sort(){
        var field = $("#field").val();
        var order = $("#order").val();
      $.get('/sort/', {field: field, order: order}, function(data){
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
    
    $(document).ready(sort());
    