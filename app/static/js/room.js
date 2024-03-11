let socketio = io();

const messages = document.querySelector("#messages");
const form = document.querySelector('#input-form')
const mapBox = document.querySelector('#map-box')

//Section needs to be revamped to maybe handle multiple server outputs with regards to formatting

const createMap = (map) => {
  const content = `<span class="map-header">MAP</span>
    <div class="map-content">
        ${map}
    </div>
    `;
  mapBox.innerHTML = content;
  console.log('map triggered')
  console.log(map)
};

const createLook = (msg) => {
  const content = `
    <div class="text">
        <span class="msg-text">
            ${msg}
        </span>
        <span class="msg-date">
                ${new Date().toLocaleString()}
        </span>
    </div>
    `;
  messages.innerHTML += content;
  if(messages.scrollHeight - messages.clientHeight - messages.scrollTop <= 60) {
    messages.scrollTop = messages.scrollHeight + 10000};
  console.log(messages.scrollHeight - messages.clientHeight - messages.scrollTop)
};

//Needs to be revamped to have one, maybe two ways of outputting server emits

socketio.on("map", (data) => {
  createMap(data.map);
});

socketio.on("event", (data) => {
  createLook(data.message);
});

//This section needs to be revamped to parse user input and package it in a uniform way so the server can handle input properly
form.addEventListener("submit", (event) => {
  event.preventDefault()
  const message = document.querySelector("#message");
  if (message.value == "") return;
  const payload = {
    command: message.value.substr(0, message.value.indexOf(" ")),
    data: message.value.substr(message.value.indexOf(" ") + 1),
  };
  if (payload.command === "" && payload.data) {
    payload.command = payload.data;
    payload.data = "";
  }
  console.log(payload);
  socketio.emit('client', payload);
  message.value = "";
  messages.scrollTop = messages.scrollHeight
})
