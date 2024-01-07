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
    //on change l'url vers l'id du dernier message (use lastMessageId)
    location.href = "#message-"+lastMessageId;

    //on autofocus l'input d'id #message
    $("#message").focus();

    setInterval(function(){
        $.get("/channels/room/"+room_id+"/messages/"+lastMessageId, function(data){
            if(data.messages.length > 0){
            //on get le nb de pixels par rapport au bas scrollé de la div de #messages-wrapper
            var scrollHeight = $("#messages-wrapper").prop("scrollHeight") - $("#messages-wrapper").scrollTop() - $("#messages-wrapper").height();

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
            
            if(scrollHeight < 50){
                //on update le dernier message
                location.href = "#message-"+lastMessageId;
                
                $("#message").focus();
            }
        });
    }, 1000);
});
