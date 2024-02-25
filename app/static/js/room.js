let socketio = io();

  const messages = document.querySelector("#messages");

  const createMessage = (username, msg) => {
    const content = `
    <div class="text">
        <span class="msg-text">
            <strong>${username}</strong>: ${msg}
        </span>
        <span class="msg-date">
                ${new Date().toLocaleString()}
        </span>
    </div>
    `;
    messages.innerHTML += content;
  };

  const createStatus = (username, msg) => {
    const content = `
    <div class="text">
        <span class="msg-text">
            ${username} ${msg}
        </span>
        <span class="msg-date">
                ${new Date().toLocaleString()}
        </span>
    </div>
    `;
    messages.innerHTML += content;
  };

  socketio.on("message", (data) => {
    createMessage(data.username, data.message);
  });

  socketio.on("status", (data) => {
    createStatus(data.username, data.message);
  });

  const sendMessage = () => {
    const message = document.querySelector("#message");
    if (message.value == "") return;
    
    socketio.emit("message", { data: message.value });
    message.value = "";
  };