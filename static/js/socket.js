// static/js/socket.js

const socket = io(); // Connect to the Socket.IO server

// Join the default room ("general")
socket.emit("join", {
    room: "general",
    user: currentUserNickname  // This should be defined in a <script> tag in your HTML
});

// Handle receiving a message
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

// Update the online user list
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

// Handle form submission (send message)
document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    if (chatForm && chatInput) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (message !== "") {
                socket.emit("send_message", {
                    room: "general",
                    sender: currentUserNickname,
                    content: message
                });
                chatInput.value = "";
            }
        });
    }
});
