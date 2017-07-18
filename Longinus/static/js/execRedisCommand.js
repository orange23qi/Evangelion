$(function(){

        $('#commandButton').click(function(){
            var redisCluster = $('#redisCluster').val()
            var redisType = $('#redisType').val()
            var commandContent = $('#commandContent').val()
            var redisDbId = $('#redisDbId').val()

            $.ajax({
            type:'POST',
            url:'/execCommand/',
            dataType: 'json',
            data:{
                "redisCluster": redisCluster,
                "redisType": redisType,
                "commandContent": commandContent,
                "redisDbId": redisDbId
            },
            success:function(data){
                var dataList    = data.data;
                var html        = '';
                var valueResult = $('#valueResult').empty();

                if (data.status > 0){
                    alert(data.msg)
                }

                if(dataList.length > 0){
                    html += '<caption>查询结果</caption>'
                    //$html += '<thead><tr><th>Command</th><th>Value</th></tr></thead><tbody>'
                    for(var i=0;i<dataList.length;i++){
                        html +='<tr><td>'+dataList[i][0]+'</td>';
                        html +='<td>'+dataList[i][1]+'</td></tr>';
                    }
                    //html += '</tbody>'

                    $('#valueResult').append(html);
                    $('#valueResult').DataTable({

                        searching:false, //去掉搜索框
                        bLengthChange:false,//去掉每页多少条框体
                        "language": {
                            "info": "", // 表格左下角显示的文字
                            "paginate": {
                                "previous": "上一页",
                                "next": "下一页"
                            }
                        },
                        destroy:true, //Cannot reinitialise DataTable,解决重新加载表格内容问题
                        columns: [
                            { title: "Key" },
                            { title: "Value" },
                        ]
                    });
                }

            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("error");
                    }
        });
        })
    })
