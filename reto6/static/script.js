async function sendMessage() {
    let userInput = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");

    if (userInput.value.trim() === "") return;

    // Mostrar el mensaje del usuario
    chatBox.innerHTML += `<div class="user-message"><b>Tú:</b> ${userInput.value}</div>`;

    // Hacer la petición al backend
    let response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput.value })
    });

    let data = await response.json();
    if (data.reply) {
        chatBox.innerHTML += `<div class="bot-message"><b>Bot:</b> ${data.reply}</div>`;
    } else {
        chatBox.innerHTML += `<div class="bot-message"><b>Bot:</b> Error al obtener respuesta</div>`;
    }

    // Limpiar input y hacer scroll
    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}
