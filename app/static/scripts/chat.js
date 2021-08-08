var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
var socket = io.connect(baseURL);

document.addEventListener('DOMContentLoaded', () => {

    var username = document.querySelector('#get-username').innerHTML;
    var room = document.querySelector('#current_room').innerHTML;

    joinRoom(room);

    socket.on('connect', function() {
        console.log('Connected to server');
    })

    socket.on('refresh', function() {
        setTimeout(function() {
        location.reload();
        }, 100);
    })

    socket.on('room-leave', function() {
        leaveRoom(room);
        socket.emit('room-change', {'room': 'Lobby'})
        setTimeout(function() {
            location.reload();
            }, 1000);
        })


    socket.on('message', data => {
            var p = document.createElement('p');
            var br = document.createElement('br');
            p.innerHTML = data['username'] + ": " + data['message'];
            if(data['username'] == username) {
                p.style.color = "red";
            }
            document.querySelector('#display-message-section').append(p);
      })

    socket.on('room-manager', data => {
        printSysMsg(data['message']);
     })

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
                socket.emit('room-change', {'room': newRoom})
                setTimeout(function() {
                    location.reload();
                    }, 50);
            }
        }
    })

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room})
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username,'room': room})
    }

   function printSysMsg(message) {
        var p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = '<i><b>' + message + '</b></i>';
        document.querySelector('#display-message-section').append(p);
   }
})

function deleteRoom(room) {
    var wantToDelete = confirm('Are you sure you want to delete this room?');
    if(wantToDelete) {
        var xhr = new XMLHttpRequest();
        sender = JSON.stringify({'room': room});
        xhr.open('POST', '/delete-room');
        xhr.send(sender);
        socket.emit('room-deleted', {'room': room})
  }
}

function clearRoom(room) {
    var wantToClear = confirm('Are you sure you want to clear the chat of this room?');
    if(wantToClear) {
        var xhr = new XMLHttpRequest();
        sender = JSON.stringify({'room': room});
        xhr.open('POST', '/clear-room');
        xhr.send(sender);
        window.location.reload();
    }
}

function removeMember(member, room) {
    var wantToRemove = confirm('Are you sure you want to remove ' + member + ' from this room?');
    if(wantToRemove) {
        var xhr = new XMLHttpRequest();
        sender = JSON.stringify({'member': member, 'room': room});
        xhr.open('POST', '/remove-member');
        xhr.send(sender);
        socket.emit('member-removed', {'member': member, 'room': room});
    }
}

