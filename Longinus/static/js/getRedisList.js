$(function(){

        $('#redisType').change(function(){
            var redisType = $('#redisType').val()

            $.ajax({
            type:'POST',
            url:'/getRedisList/',
            dataType: 'json',
            data:{
                "redisType": redisType
            },
            success:function(data){
                var dbList = data.data
                var $html = '';
                var $redisCluster = $('#redisCluster').empty();

                if(dbList.length > 0){
                    $('#redisCluster').html('');

                    for(var i=0;i<dbList.length;i++){
                        $html +='<option>'+dbList[i]+'</option>';
                    }

                    $('#redisCluster').append($html);
                }

                if(redisType == "Master-Slave"){
                    $("#redisDb").show();
                } else { 
                    $("#redisDb").hide();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                        console.log("error");
                   }
        });
        })
    })
