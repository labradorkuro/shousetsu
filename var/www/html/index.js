$(function(){
    var ajax ={
         _url : 'nsl1_wifi.php'
        ,_method : 'post'
        ,_type : 'json'
        ,_param : {}
        ,request : function(){
            var defer = $.Deferred();
            $.ajax({
                 type : this._method
                ,cache : false
                ,url : this._url
                ,data : this._param
                ,dataType : this._type
                ,success : defer.resolve
                ,error : defer.reject
            });
            return defer.promise();
        }
    };

    $('body')
        .on('click',function(){
            $('#wifi_list').hide();
        })
        .on('click','#wifi_dropdown',function(){
            $('#wifi_list').css({
                 top : ($('#ssid').offset().top + $('#ssid').outerHeight(true)) + 'px'
                ,left : $('#ssid').offset().left + 'px'
            })
                .width($('#ssid').outerWidth(true))
                .show();
            return false;
        })
        .on('click','#wifi_list div',function(){
            $('#ssid').val($(this).text());
        })
        .on('click','#update',function(){
            $('#ssid,#pass').removeClass('txt_error');
            if (!($('#ssid').val() && $('#pass').val())){
                var msg = '';
                if (!$('#ssid').val()){
                    msg = 'SSIDを入力してください。<br>';
                    $('#ssid').addClass('txt_error');
                }
                if (!$('#pass').val()){
                    msg += 'パスワードを入力してください。<br>';
                    $('#pass').addClass('txt_error');
                }
                $('#msg').addClass('error').html(msg);
                $('#msg_section').fadeIn(1000,function(){
                    setTimeout(function(){
                        $('#msg_section').fadeOut(1000,function(){
                            $('#msg').removeClass('error')
                        });
                    },2000);
                });
                return false;
            }
            setTimeout(function(){
                ajax._param = {
                     update   : 1
                    ,input1 : $('#ssid').val()
                    ,input2 : $('#pass').val()
                }
                ajax.request();
                $('#msg').text('センサーの接続設定を行いました。\nセンサー再起動してください。');
            },500);
        });


});
