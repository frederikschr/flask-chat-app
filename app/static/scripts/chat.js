document.addEventListener('DOMContentLoaded', () => {
    var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
    var socket = io.connect(baseURL);

    var username = document.querySelector('#get-username').innerHTML;

    var room = "Lobby";
    joinRoom (room);

    socket.on('connect', function() {
        console.log('Connected to server');
    })

    socket.on('message', data => {
            var p = document.createElement('p');
            var br = document.createElement('br');
            p.innerHTML = data['username'] + ": " + data['message'];
            document.querySelector('#display-message-section').append(p);
      })

     socket.on('room-manager', data => {
        printSysMsg(data['message']);
     })

    //Send button clicked
    document.querySelector('#send_message').onclick = () => {
    socket.send({'message': document.querySelector('#user_message').value, 'room': room});
    document.querySelector('#user_message').value = '';
    }

    document.querySelectorAll('.select-room').forEach(button => {
        button.onclick = () => {
            var newRoom = button.innerHTML;
            if (newRoom == room) {
                printSysMsg('You are already in the ' + room + 'room.');
            }
            else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    })

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room})
        document.querySelector('#display-message-section').innerHTML = '';
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username,'room': room})
    }

   function printSysMsg(message){
        var p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = '<i>' + message + '</i>';
        document.querySelector('#display-message-section').append(p);
   }

})