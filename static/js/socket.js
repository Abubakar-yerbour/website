// static/js/socket.js

const socket = io(); // Connect to Socket.IO

socket.on("connect", () => {
    console.log("🔌 Connected to chat server.");
});

// Receive a new message
socket.on("receive_message", (data) => {
    const chatBox = document.getElementById("chat-box");
    if (chatBox) {
        const div = document.createElement("div");
        div.className = "msg-line";
        div.innerHTML = `<strong>@${data.sender}:</strong> ${data.content}`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

// Update online users
socket.on("update_users", (userList) => {
    const list = document.getElementById("online-users");
    if (list) {
        list.innerHTML = "";
        userList.forEach(nick => {
            const li = document.createElement("li");
            li.textContent = `@${nick}`;
            list.appendChild(li);
        });
    }
});
