//alert("register.js")
//// 确保被调用弹出。想当于被register.html文件里加载了
//整个网页加载完毕之后，再执行 #相当于id  找到id=captcha-btn标签
// name再input标签里 input[name='email']
// $ jQuery缩写 this表示当前的captcha-btn对象  加$ jquery按钮对象

function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event){

        // $this 代表当前按钮的jQuery对象
       var $this = $(this);

    // 阻止默认事件 防止点击这个按钮，提交整个表单form的操作
        event.preventDefault();
    // 获取用户输入的邮箱 ，先找到邮箱输入框 获取name $("input[name='email']")获取输入框 .val() 获取里面输的值
        var email = $("input[name='email']").val();
        $.ajax({
            // 当前文件就有http;//5000
            // /author/captcha/email?email=xx@qq.com
            url: "/author/captcha/email?email="+email,
            method: 'GET',
            success: function (result){
                var code = result['code'];
                if (code == 200){
                    var countdown = 5;

                    //倒计时之前；不能点击按钮，取消点击事件
                    $this.off("click");
                    // 倒计时结束执行
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown -= 1;
                        if (countdown <= 0){
                            //清除定时器
                            clearInterval(timer);
                            //将按钮重新显示
                            $this.text("获取验证码");
                            //重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    alert("邮箱验证码发送成功！")
                }else{
                    alert(result['message'])
                }
            },
            fail: function (error){
                console.log(error);
        }
    })
    });
}


// 整个页面加载之后运行
$(function(){
    bindEmailCaptchaClick();
});

//$(function () {
//    $("#captcha-btn").click(function (event){
//
//        // $this 代表当前按钮的jQuery对象
//       var $this = $(this);
//
//    // 阻止默认事件 防止点击这个按钮，提交整个表单form的操作
//    event.preventDefault();
//    // 获取用户输入的邮箱 ，先找到邮箱输入框 获取name $("input[name='email']")获取输入框 .val() 获取里面输的值
//    var email = $("input[name='email']").val();
//    $.ajax({
//        // 当前文件就有http;//5000
//        // /author/captcha/email?email=xx@qq.com
//        url: "/author/captcha/email?email="+email,
//        method: 'GET',
//        success: function (result){
//            var code = result['code'];
//            if (code == 200){
//                var countdown = 60;
//
//                //倒计时之前；不能点击按钮，取消点击事件
//                $this.off(e:"click");
//                // 倒计时结束执行
//                var timer = setInterval(handler:function(){
//                    $this.text(countdown);
//                    countdown -= 1;
//                    if (countdown <= 0){
//                        //清除定时器
//                        clearInterval(timer);
//                        //将按钮重新显示
//                        $this.text("获取验证码");
//                        //重新绑定点击事件
//
//                    }
//                }, timeout:1000);
//                alert("邮箱验证码发送成功！")
//            }else{
//                alert(result['message'])
//            }
//        },
//        fail: function (error){
//            console.log(error);
//        }
//    })
//    });
//});