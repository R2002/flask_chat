$(document).ready(function() {
    // connect
    var socket = io.connect();
    socket.on('connect', function() {
        $('#filter-loading').slideUp(700);
    });

    // ログインパケット受信
    socket.on('login_confirm', function(data) {
        if('confirm' in data){
            $('#filter-loading').slideUp(700);
        }
    });

    // メッセージ受信
    socket.on('my_response', function(data) {
        let item = document.createElement('div');
        item.innerHTML = recieve_html(data);
        messages.insertBefore(item, messages.firstElementChild);
    });

    // メッセージ送信
    $('form#form').submit(function(event) {
        // 内容があれば送信
        if($('#input').val()) {
            socket.emit('send_message', {comment: $('#input').val()});
            // input内容削除
            $('#input').val("");
        }
        // submitさせない
        return false;
    });
});

// 受信形式設定
function recieve_html(data) {
    html = '<div style="text-align:left; margin-top:8px;">'+"\n";
    html += '<strong>'+data['name']+' <font style="color:#aaa;">#'+data['user_id']+'</font></strong>'+"\n";
    html += '<font style="color:#ccc; font-size:80%; margin-left:20px;">'+data['date']+'</font><br>'+"\n";
    html += data['comment']+"\n";
    html += '</div>'+"\n";
    return html;
}