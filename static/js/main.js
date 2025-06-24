// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const currentTheme = localStorage.getItem("ug-theme") || "light";

    document.documentElement.setAttribute("data-theme", currentTheme);

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            let current = document.documentElement.getAttribute("data-theme");
            let nextTheme = current === "light" ? "dark" : "light";
            document.documentElement.setAttribute("data-theme", nextTheme);
            localStorage.setItem("ug-theme", nextTheme);
        });
    }

    const chatForm = document.getElementById("chat-form");
    const folderChatForm = document.getElementById("folder-chat-form");

    // General Chat Submission
    if (chatForm) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const input = document.getElementById("chat-input");
            if (input.value.trim() !== "") {
                socket.emit("send_message", { room: "general", content: input.value });
                input.value = "";
            }
        });
    }

    // Folder Chat Submission
    if (folderChatForm) {
        folderChatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const input = document.getElementById("folder-chat-input");
            const room = folderChatForm.getAttribute("data-room");
            if (input.value.trim() !== "") {
                socket.emit("send_message", { room: room, content: input.value });
                input.value = "";
            }
        });
    }
});
