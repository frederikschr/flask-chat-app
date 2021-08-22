var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
var socket = io.connect(baseURL);

function reload(delay) {
     setTimeout(function() {
        location.reload();
        }, delay);
}

document.addEventListener('DOMContentLoaded', () => {

    var username = document.querySelector('#get-username').innerHTML;
    var room = document.getElementById('get-room').innerHTML;

    joinRoom(room);

    socket.on('connect', function() {
        console.log('Connected to server');
    })

    socket.on('refresh', function() {
        reload(500);
    })

    socket.on('room-leave', function() {
        leaveRoom(room);
        socket.emit('room-change', {'room': 'Lobby'})
        reload(200);
    })

    socket.on('message', data => {
            var p = document.createElement('p');
            var br = document.createElement('br');
            p.innerHTML = data['username'] + ": " + data['message'];
            if(data['username'] == username) {
                p.style.color = "red";
                p.setAttribute("class", "own-message");
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
                reload(50);
            }
        }
    })

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
    }

    function leaveRoom(room) {
        socket.emit('leave', {'username': username,'room': room});
    }

   function printSysMsg(message) {
        var p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = '<i><b>' + message + '</b></i>';
        document.querySelector('#display-message-section').append(p);
   }
})

function addMember(room) {
    var newMember = document.getElementById('added-member').value;
    socket.emit('member-added', {'new_member': newMember, 'room': room});
}

function deleteRoom(room) {
    var wantToDelete = confirm('Are you sure you want to clear the chat of this room?');
    if(wantToDelete) {
        socket.emit('room-deleted', {'room': room});
    }
}

function clearRoom(room) {
    var wantToClear = confirm('Are you sure you want to clear the chat of this room?');
    if(wantToClear) {
        socket.emit('room-cleared', {'room': room});
    }
}

function removeMember(member, room) {
    var wantToRemove = confirm('Are you sure you want to remove ' + member + ' from this room?');
    if(wantToRemove) {
        socket.emit('member-removed', {'member': member, 'room': room});
    }
}
