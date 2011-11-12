%include head

<div id="wrapper">
    %if uid and name:
    <div id="user">
        <p>你好, {{name}}, <a href="/logout">退出</a></p>
    </div>
    %end
    <center>
        <h1>北航神秘树洞</h1>
    </center>
    <div id="notice">{{notice}}</div>
    
    <p>小朋友, 有什么想要说的吗?</p>
    
    <form id="what2say" action="/say" method="post">
        
        <p><textarea name="word"></textarea></p>
        <p><input type="checkbox" name="toweiqun" />&nbsp;同时发送到<a href="http://q.weibo.com/168175" target="__blank">北京航空航天大学微群</a></p>
        <p><input type="submit" value="写好了, 丢进树洞" /> &nbsp; 去<a href="http://weibo.com/buaatreeholes" target="__blank">@北航神秘树洞</a>看看别人说了什么</p>
        <input type="hidden" name="formhash" value="{{formhash}}" />
    </form>
    <br/>
    <!--<p>关注<a href="/follow">@北航神秘树洞</a></p>-->
    <br/>
    
    %include info
</div>
<script type="text/javascript">
    var notice = document.getElementById("notice");
    if (notice.innerHTML) {
        notice.style.display = "block";
        setTimeout(function(){notice.style.display = "none";}, 5 * 1000);
    }
</script>

%include foot
