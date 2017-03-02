function sort(cat){
        var params = get_params();
        //alert(params['search']);
        //alert($('#search').val());
        $('#search').val(params['search']);
        //alert($('#search').val());
        var search = params['search'];
        if (search == ""){
            
        };
    
        var field = $("#field").val();
        var order = $("#order").val();
        
        if (cat == undefined){
            var category = window.location.href.split('#')[1];
        }else{
            var category = cat.split('#')[1];
        };
    
        if (category == undefined){
            category = '-1';
        };
    
      $.get('/sort/', {field: field, order: order, category: category, search: search}, function(data){
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
        
        var url = window.location.href.split('#')[1];
        if (url == undefined){
            url = '#-1';
        };
        //alert(url);
        
        $('.nav-link').each(function(){
            //alert($(this).attr('href') + '  ==  ' + window.location.href);
           

           if ($(this).attr('href') == url){
               //alert($(this).attr('href'));
               $(this).parent().addClass('active'); 
               flag_active = true
           } else {
               $(this).parent().removeClass('active');
               //alert('else'+$(this).attr('href'));
           };
       });   
    };


    function get_params(){
        var params = window
        .location
        .search
        .replace('?','')
        .split('#')[0]
        .split('&')
        .reduce(
            function(p,e){
                var a = e.split('=');
                p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
                return p;
        },
        {}
    );
        return params;
    }

    //$(document).ready(sort());
    //$(document).ready(set_active_nav_link());

    $(document).ready(function(){
        
        set_active_nav_link();
        sort();
        
        
       $('.nav-link').click(function(){
           $('.nav-link').each(function(){
               $(this).parent().removeClass('active');
           });                  
           
           $(this).parent().addClass('active');
           sort(this.href);
       });
    });
    
    