
const new_chat_button = document.querySelector(".new-chat");
const models = document.querySelectorAll(".model-selector button");

for (const model of models) {
    model.addEventListener("click", function () {
        document.querySelector(".model-selector button.selected")?.classList.remove("selected");
        model.classList.add("selected");
    });
}

const message_box = document.querySelector("#message");

function show_view(view_selector) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

new_chat_button.addEventListener("click", function () {
    show_view(".new-chat-view");
});

document.querySelectorAll(".conversation-button").forEach(button => {
    button.addEventListener("click", function () {
        show_view(".conversation-view");
    })
});

const sendButton = document.querySelector("#send-btn");

document.getElementById('send-btn').addEventListener('click', function() {
    var inputText = document.getElementById('message').value;
    document.getElementById('initialQuestion').value = inputText; 
    if (inputText.trim() !== "") {
        addMessage('user', inputText);

        fetchJurisprudencias(inputText);

        document.getElementById('message').value = '';
        scrollToEnd();
    }
});

async function fetchJurisprudencias(query) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/buscar_jurisprudencias/?texto=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error('Falha na busca de jurisprudências');
        }
        const jurisprudencias = await response.json();
        displayJurisprudencias(jurisprudencias);
    } catch (error) {
        console.error('Erro ao buscar jurisprudências:', error);
        addMessage('assistant', 'Não foi possível encontrar jurisprudências relacionadas à sua busca.');
    }
}

function displayJurisprudencias(jurisprudencias) {
    let contentHtml = `<p>Jurisprudências encontradas:</p><form id="jurisprudenciasForm">`;
    jurisprudencias.forEach(juris => {
        const cleanedText = cleanText(juris.texto);
        contentHtml += `<label><input type="checkbox" name="jurisprudencia" value="${cleanedText}"> ${cleanedText} </label><br>`;
    });
    contentHtml += `<button type="button" onclick="generateDefense()">GERAR DEFESA JURÍDICA</button></form>`;
    addMessage('assistant', contentHtml);
}

function cleanText(text) {
    if (text.startsWith('>')) {
        text = text.substring(1);
    }
    return text.trim();
}

function generateDefense() {
    var form = document.getElementById("jurisprudenciasForm");
    var selectedItems = form.querySelectorAll('input[type="checkbox"]:checked');
    var selectedJurisprudencias = Array.from(selectedItems).map(item => item.value);

    if (selectedJurisprudencias.length === 0) {
        alert("Por favor, selecione ao menos uma jurisprudência para continuar.");
        return;
    }

    var initialQuestion = document.getElementById("initialQuestion").value;
    var prompt = createPrompt(initialQuestion, selectedJurisprudencias);
    fetchGeneratedResponse(prompt);
}

function createPrompt(question, jurisprudencias) {
    let intro = `Baseado na pergunta inicial:
    "${question}" e nas seguintes jurisprudências,
    elabore uma argumentação detalhada e analítica
    para uma defesa jurídica:`;

    let content = jurisprudencias.join("\n\n");

    return `${intro}\n\n${content}`;
}

function fetchGeneratedResponse(prompt) {
    fetch('http://127.0.0.1:8000/gerar_defesa/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        addMessage('assistant', data.response || "Desculpe, não consegui gerar uma defesa com as informações fornecidas.");
    })
    .catch(error => {
        console.error('Erro ao solicitar a geração de defesa:', error);
        addMessage('assistant', 'Erro ao conectar ao serviço de geração de defesa.');
    });
}

function addMessage(sender, messageText) {
    var messageDiv = document.createElement('div');
    messageDiv.className = sender + " message";
    var identityDiv = document.createElement('div');
    identityDiv.className = "identity";
    var userIcon = document.createElement('i');
    userIcon.className = sender === 'user' ? 'user-icon' : 'gpt user-icon';
    userIcon.textContent = sender === 'user' ? 'u' : 'G';
    var contentDiv = document.createElement('div');
    contentDiv.className = "content";
    contentDiv.innerHTML = messageText;

    identityDiv.appendChild(userIcon);
    messageDiv.appendChild(identityDiv);
    messageDiv.appendChild(contentDiv);
    document.querySelector('.conversation-view').appendChild(messageDiv);

    scrollToEnd();
}

function scrollToEnd() {
    var elements = document.querySelectorAll('.conversation-view .message');
    var lastElement = elements[elements.length - 1];
    lastElement.scrollIntoView({ behavior: 'smooth' });
}