const axios = require("axios");

async function getMedicalAdviceFromChatGPT(symptoms) {
    const apiKey = process.env.OPENAI_API_KEY;
    const endpoint = "https://api.openai.com/v1/chat/completions";

    const requestBody = {
        model: "gpt-4",
        messages: [
            { role: "system", content: "You are a medical assistant providing advice based on symptoms." },
            { role: "user", content: `I have the following symptoms: ${symptoms}. Suggest possible causes, over-the-counter medications, side effects, and home remedies.` }
        ]
    };

    try {
        const response = await axios.post(endpoint, requestBody, {
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            }
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error("Error fetching AI response:", error);
        return "Sorry, I couldn't process your request.";
    }
}

module.exports = { getMedicalAdviceFromChatGPT };
