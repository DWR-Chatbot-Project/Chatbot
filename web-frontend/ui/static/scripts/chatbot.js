const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const modelSelect = get(".msger-select");
const isUserVerified = false;

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "../static/icons/dialogflow-insights-svgrepo-com.svg";
const PERSON_IMG = "";

let BOT_NAME = "    ChatBot";
let PERSON_NAME = "You";

msgerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    const selectedModel = modelSelect.value;

    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
    msgerInput.value = "";

    botResponse(msgText, selectedModel);
});

function appendMessage(name, img, side, text) {
    //   Simple solution for small apps
    const msgHTML = `
                <div class="msg ${side}-msg">
                <div class="msg-img" style="background-image: url(${img})"></div>
                <div class="msg-bubble">
                    <div class="msg-info">
                        <div class="msg-info-name">${name}</div>
                        <div class="msg-info-time">${formatDate(
                            new Date()
                        )}</div>
                    </div>

                    <div class="msg-text">${text}</div>
                </div>
                </div>
            `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

async function botResponse(text, selectedModel) {
    // Bot Response
    try {
        const response = await fetch(
            `reply?input=${text}&modelName=${selectedModel}`
        );
        const data = await response.json();
        let reply = data.bot_reply;
        if (selectedModel == "bloom") {
            reply = reply.response;
        }
        appendMessage(BOT_NAME + " - " + selectedModel, BOT_IMG, "left", reply);
    } catch (error) {
        console.error(error);
        appendMessage(
            BOT_NAME + "- " + selectedModel,
            BOT_IMG,
            "left",
            "Sorry, I'm not able to respond at the moment."
        );
    }
}

// async function authenticate(token) {
//     const response = await fetch(`login?token=${token}`, {
//         method: "POST",
//     });

//     const data = await response.json();
//     console.log("data", data);

//     if ("error" in data) {
//         error = response.json()["error"];
//         appendMessage(BOT_NAME, BOT_IMG, "left", error["message"]);
//     } else {
//         isUserVerified = true;
//         appendMessage(BOT_NAME, BOT_IMG, "left", "How can I can help you?");
//     }
// }

// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}
