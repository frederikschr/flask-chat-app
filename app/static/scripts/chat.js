document.addEventListener('DOMContentLoaded', () => {
    var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
    var socket = io.connect(baseURL);

    socket.on('connect', function() {
        console.log('Connected to server');
    })

    socket.on('message', data => {
            var p = document.createElement('p');
            var br = document.createElement('br');
            p.innerHTML = data['username'] + ": " + data['message'];
            document.querySelector('#display-message-section').append(p);
      })

    //Send button clicked
    document.querySelector('#send_message').onclick = () => {
    socket.send({'message': document.querySelector('#user_message').value});
    document.querySelector('#user_message').value = '';
    }
})