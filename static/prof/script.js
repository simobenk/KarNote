// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})


var recognition = new webkitSpeechRecognition();
recognition.lang = 'fr-FR';
recognition.continuous = true;
recognition.interimResults = true;

// Accumuler la transcription ici
var accumulated_transcript = '';

recognition.onresult = function(event) {
	var interim_transcript = '';
	var final_transcript = '';

	for (var i = event.resultIndex; i < event.results.length; ++i) {
	if (event.results[i].isFinal) {
		final_transcript += event.results[i][0].transcript;
	} else {
		interim_transcript += event.results[i][0].transcript;
	}
	}
	accumulated_transcript += final_transcript;  // Accumuler le texte final
	document.getElementById('transcription').textContent = accumulated_transcript + interim_transcript;
};

recognition.onend = function() {
	recognition.stop();  // Redémarrer la reconnaissance après chaque arrêt
};

document.getElementById('start-button').addEventListener('click', function() {
	recognition.start();
});

document.getElementById('stop-button').addEventListener('click', function() {
	recognition.stop();
});

document.getElementById('stop-button').addEventListener('click', function() {
	var text = document.getElementById('transcription').textContent;
	var blob = new Blob([text], { type: 'text/plain' });
	var anchor = document.createElement('a');
	anchor.download = "transcription.txt";
	anchor.href = window.URL.createObjectURL(blob);
	anchor.target = '_blank';
	anchor.style.display = 'none'; // just to be safe!
	document.body.appendChild(anchor);
	anchor.click();
	document.body.removeChild(anchor);


	// Submit the form with the transcription
	document.getElementById('hidden-transcription').value = accumulated_transcript;
	document.getElementById('transcription-form').submit();
});
function sendVariable() {
    let jsVariable = document.getElementById('transcription').textContent;  // Votre variable texte

    fetch('/receive_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ js_variable: jsVariable })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Affiche le statut de la réponse et la donnée reçue
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const importButton = document.getElementById('import-pdf');
    const pdfTableBody = document.querySelector('pdf-table');
    const fileInput = document.getElementById('file-input');

    importButton.addEventListener('click', function () {
        // Déclencher l'événement de clic sur l'input de type "file"
        fileInput.click();
    });

    // Ajouter un écouteur d'événements pour le changement de fichier
    fileInput.addEventListener('change', function () {
        // Vérifier si un fichier est sélectionné
        if (fileInput.files.length > 0) {
            // Récupérer le fichier sélectionné
            const file = fileInput.files[0];
            
            // Créer une nouvelle ligne dans le tableau
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
                <td>${file.name}</td>
                <td>${(file.size / 1024).toFixed(2)} KB</td>
                <td>${file.type}</td>
            `;

            // Ajouter la nouvelle ligne au tableau
            pdfTableBody.appendChild(newRow);
        }
    });
});

const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
let userMessage = null; // Variable to store user's message

// Utiliser plutôt la fonction getApiKey() que nous avons créée précédemment
async function getApiKey() {
    try {
        const response = await fetch('/api/get-openai-key');
        const data = await response.json();
        return data.apiKey;
    } catch (error) {
        console.error('Error fetching API key:', error);
        return null;
    }
}

const inputInitHeight = chatInput.scrollHeight;
const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', () => {
        const message = userInput.value;
        if (message.trim()) {
            appendMessage('You', message);
            userInput.value = '';
            sendMessageToGemini(message);
        }
    });

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendBtn.click();
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = `${sender}: ${message}`;
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    async function sendMessageToGemini(message) {
        try {
            const response = await fetch('/api/get-gemini-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            appendMessage('Gemini', data.reply);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('System', 'Error communicating with Gemini');
        }
    }
});
const handleChat = async () => {
    const apiKey = await getApiKey();
    if (!apiKey) {
        console.error('Failed to get API key');
        return;
    }
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;
    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;
    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}
chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});
chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});
sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

function loadFiles() {
    fetch('/get_files')
    .then(response => response.json())
    .then(files => {
        const tableBody = document.querySelector('#fileTable tbody');
        tableBody.innerHTML = '';
        files.forEach(file => {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.textContent = file;
            row.appendChild(cell);
            tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching files:', error));
}

// Initial load of files
loadFiles();