const id = JSON.parse(document.getElementById('json-otheruser-id').textContent);
const sender = JSON.parse(document.getElementById('json-requestusername').textContent);
const receiver = JSON.parse(document.getElementById('json-otherusername').textContent);


    // when running in development use this:
    
    



    let ws_path;

    if (window.location.protocol === 'https:') {
        ws_path = 'wss://' + window.location.host + '/wss/chat/' + id;
    } else {
        ws_path = 'ws://' + window.location.host + '/ws/chat/' + id;
    }
    
    const parts = window.location.href.split('?');
    if (parts.length == 2) {
        ws_path += '/?' + parts[1];
    }

    socket = new WebSocket(ws_path);

    socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
    }

    socket.onclose = function(e){
        console.log("CONNECTION LOST");
    }

    socket.onerror = function(e){
        console.log("ERROR OCCURED");
    }
    
    socket.onmessage = function(e){
        const data = JSON.parse(e.data);
        if(data.sender === sender){
            document.querySelector('#chat-body').innerHTML += `<div class="me message" >
                                            <div class="text-main">
                                                <div class="me text-group">
                                                    <div class="me text">
                                                        <p>
                                                            ${data.message}
                                                        </p>
                                                    </div>
                                                </div>
                                                <span></span>
                                            </div>
                                        </div>`
        }else{
            document.querySelector('#chat-body').innerHTML += `<div class="message" >
                                            <!-- DONT FORGET TO PUT PROFILE PICTURE -->
                                            <div class="text-main">
                                                <div class="text-group">
                                                    <div class="text" >
                                                        <p>
                                                            ${data.message}
                                                        </p>
                                                    </div>
                                                </div>
                                                <span></span>
                                            </div>
                                        </div>`
        }}

    document.querySelector('#message_input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };
    
    document.querySelector('#chat-message-submit').onclick = function(e){
        e.preventDefault();
        console.log(sender);
        const message_input = document.querySelector('#message_input');
        const message = message_input.value;
        socket.send(JSON.stringify({
            'message':message,
            'sender':sender,
            'receiver':receiver
        }));
        message_input.value = '';
}