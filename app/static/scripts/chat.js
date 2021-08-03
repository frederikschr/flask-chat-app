document.addEventListener('DOMContentLoaded', () => {
    var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
    var socket = io.connect(baseURL);

    var username = document.querySelector('#get-username').innerHTML;

    var room = document.querySelector('#current_room').innerHTML;
    joinRoom(room);

    socket.on('connect', function() {
        console.log('Connected to server');
    })

    socket.on('message', data => {
            var p = document.createElement('p');
            var br = document.createElement('br');
            p.innerHTML = data['username'] + ": " + data['message'];
            p.style.color = "red";
            document.querySelector('#display-message-section').append(p);
      })

     socket.on('room-manager', data => {
        printSysMsg(data['message']);
     })

    //Send button clicked
    document.querySelector('#send_message').onclick = () => {
    socket.send({'message': document.querySelector('#user_message').value, 'username': username, 'room': room});
    document.querySelector('#user_message').value = '';
    }

    document.querySelectorAll('.select-room').forEach(button => {
        button.onclick = () => {
            var newRoom = button.innerHTML;
            if (newRoom == room) {
                printSysMsg('You are already in the ' + room + ' room.');
            }
            else {
                leaveRoom(room);
                joinRoom(newRoom);
                setTimeout(function() {
                    location.reload();
                    }, 50);
            }
        }
    })

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room})
        //document.querySelector('#display-message-section').innerHTML = '';
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username,'room': room})
    }

   function printSysMsg(message) {
        var p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = '<i>' + message + '</i>';
        //document.querySelector('#display-message-section').append(p);
   }
})

function deleteRoom(room) {
    console.log(room);
    var wantToDelete = confirm('Are you sure you want to delete this room?');
    if(wantToDelete) {
        var xhr = new XMLHttpRequest();
        sender = JSON.stringify({'room': room});
        xhr.open('POST', '/delete-room');
        xhr.send(sender);
        window.location.reload();

  }
}
