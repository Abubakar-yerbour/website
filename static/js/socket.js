// static/js/socket.js

const socket = io(); // Connect to the Socket.IO server

document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    // Get current user nickname from a hidden element or global variable
    const currentUserNickname = document.body.getAttribute("data-nick");

    // Join the chat room
    socket.emit("join", {
        room: "general",
        user: currentUserNickname
    });

    // Submit new message
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

    // Receive a new message
    socket.on("receive_message", (data) => {
        const div = document.createElement("div");
        div.className = "msg-line";
        div.innerHTML = `<strong>@${data.sender}:</strong> ${data.content}`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
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
});
