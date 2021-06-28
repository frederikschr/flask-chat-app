document.addEventListener('DOMContentLoaded', () => {
    var baseURL = location.protocol + '//' + document.domain + ':' + location.port;
    var socket = io.connect(baseURL);

    socket.on('connect', function() {
        console.log('here');
        socket.emit('my event', {data: 'I\'m connected!'});
        })

})