function addMessage(message) {
    $("#messages").append(
        "<div class=\"message\">"+
            "<div class=\"message__header\">"+
                "<div class=\"message__author\">"+message.user+"</div>"+
                "<div class=\"message__date\">"+message.date+"</div>"+
            "</div>"+
            "<div class=\"message__text\">"+message.message+"</div>"+
        "</div>"
    )
}

$(document).ready(function(){
    setInterval(function(){
        $.get("/channels/room/"+room_id+"/messages/"+lastMessageId, function(data){
            if(data.length == 0) return;

            for (let j = data.length; j > 0; j--) {
                addMessage(data[j-1]);
            }

            lastMessageId = data[0].id;
        });
    }, 1000);
});
