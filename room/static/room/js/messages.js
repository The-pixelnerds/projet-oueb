function addMessage(message) {
    var deleteButton = "<button class=\"message__remove\" onclick=\"sendDelete("+message.id+")\"></button>"

    $("#messages").append(
        "<div id=\"message-"+message.id+"\" class=\"message notyours\">"+
            "<div class=\"message__header\">"+
                "<div class=\"message__author\">"+message.user+"</div>"+
                "<div class=\"message__date\">"+message.date+"</div>"+
            "</div>"+
            "<div class=\"message__text\">"+message.message+"</div>"+
            (message.candelete ? deleteButton : "")+
        "</div>"
    )
}

function sendDelete(id){
    $.get("/channels/room/delete/"+id, function(data){
        if(data.status == "ok") {
            $("#message-"+id).remove();
        }
    });
}

$(document).ready(function(){
    setInterval(function(){
        $.get("/channels/room/"+room_id+"/messages/"+lastMessageId, function(data){
            if(data.messages.length > 0){
                for (let j = data.messages.length; j > 0; j--) {
                    addMessage(data.messages[j-1]);
                }

                lastMessageId = data.messages[0].id;
            }

            if(data.deletes.length > 0){
                for (let j = data.deletes.length; j > 0; j--) {
                    $("#message-"+data.deletes[j-1]).remove();
                }
            }
        });
    }, 1000);
});
