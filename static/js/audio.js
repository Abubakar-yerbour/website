// static/js/audio.js

let localStream = null;
let peerConnections = {};
const config = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

const socket = io("/voice");  // separate namespace for voice chat
const joinBtn = document.getElementById("join-voice");
const micToggleBtn = document.getElementById("toggle-mic");
const audioEl = document.getElementById("voice-audio");

joinBtn?.addEventListener("click", async () => {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        socket.emit("join_voice");

        socket.on("offer", async ({ from, offer }) => {
            const pc = new RTCPeerConnection(config);
            peerConnections[from] = pc;

            localStream.getTracks().forEach(track => pc.addTrack(track, localStream));

            pc.ontrack = (event) => {
                audioEl.srcObject = event.streams[0];
            };

            await pc.setRemoteDescription(new RTCSessionDescription(offer));
            const answer = await pc.createAnswer();
            await pc.setLocalDescription(answer);
            socket.emit("answer", { to: from, answer });
        });

        socket.on("answer", ({ from, answer }) => {
            peerConnections[from]?.setRemoteDescription(new RTCSessionDescription(answer));
        });

        socket.on("ice-candidate", ({ from, candidate }) => {
            if (candidate) {
                peerConnections[from]?.addIceCandidate(new RTCIceCandidate(candidate));
            }
        });

        socket.on("user-joined", async (userId) => {
            const pc = new RTCPeerConnection(config);
            peerConnections[userId] = pc;

            localStream.getTracks().forEach(track => pc.addTrack(track, localStream));

            pc.onicecandidate = (event) => {
                if (event.candidate) {
                    socket.emit("ice-candidate", { to: userId, candidate: event.candidate });
                }
            };

            pc.ontrack = (event) => {
                audioEl.srcObject = event.streams[0];
            };

            const offer = await pc.createOffer();
            await pc.setLocalDescription(offer);
            socket.emit("offer", { to: userId, offer });
        });
    } catch (err) {
        console.error("Microphone access failed:", err);
        alert("Microphone access is required to join voice chat.");
    }
});

micToggleBtn?.addEventListener("click", () => {
    if (localStream) {
        const audioTrack = localStream.getAudioTracks()[0];
        audioTrack.enabled = !audioTrack.enabled;
        micToggleBtn.textContent = audioTrack.enabled ? "🎙️ Mute" : "🔇 Unmute";
    }
});
