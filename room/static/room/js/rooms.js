function addRoom(room) {
    let str = "";
    if(room.id == room_id){
        str = "<a href=\"/channels/room/"+room.id+"\" id=\"selected\"><b>"+ room.name+"</b></a><br>";
    }else{
        str = "<a href=\"/channels/room/"+room.id+"\">"+ room.name+"</a><br>";
    }
    str += "\n"
    
    $("#rooms").append(str)
}

$(document).ready(function(){
    setInterval(function(){
        $.get("/channels/room/rooms", function(data){
            //on remove les rooms
            $("#rooms").empty();
            
            let isStillExist = false;
            for (let j = 0; j < data.length; j++) {
                addRoom(data[j]);
                if(data[j].id == room_id) isStillExist = true;
            }
            if(!isStillExist && room_id!=-1) window.location.href = "/channels/";
        });
    }, 5000);
});