%include head

<div id="wrapper">
    <center>
        <h1>北航神秘树洞</h1>
    </center>
    <div id="notice">{{!notice}}</div>
    
    <p>
        <ul>
            <li>想吐槽?</li>
            <li>有心事无人诉说?</li>
            <li>留下匿名小纸条?</li>
            <li>喜欢树洞的感觉?</li>
        </ul>
    </p>
    
    <p>
        让<a href="http://weibo.com/buaatreeholes">@北航神秘树洞</a>帮你说出来吧!
    </p>
    
    <p>
        <a href="/auth"><img src="/static/login240.png" /></a>
    </p>
    
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
