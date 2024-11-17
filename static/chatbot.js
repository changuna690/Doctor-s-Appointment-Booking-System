function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    
    if (userInput !== '') {
      appendUserMessage(userInput);
      generateBotReply(userInput);
      document.getElementById('user-input').value = '';
    }
  }
  
  function appendUserMessage(message) {
    var chatContainer = document.querySelector('.chatbot-container');
    var userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');
    userMessageElement.textContent = message;
    chatContainer.appendChild(userMessageElement);
  }
  
  function appendBotMessage(message) {
    var chatContainer = document.querySelector('.chatbot-container');
    var botMessageElement = document.createElement('div');
    botMessageElement.classList.add('bot-message');
    botMessageElement.textContent = message;
    chatContainer.appendChild(botMessageElement);
  }
  
  function generateBotReply(userInput) {
    var botReply;
    
    // Define different responses based on user input
    if (userInput.toLowerCase().includes('hello')) {
        botReply = "Hi there! How can I assist you today?";
    } else if (userInput.toLowerCase().includes('how are you')) {
        botReply = "I'm just a bot, but thanks for asking!";
    } else if (userInput.toLowerCase().includes('help')) {
        botReply = "Sure, I'm here to help. What do you need assistance with?";
    } else if (userInput.toLowerCase().includes('available')) {
      botReply = "you can go through the vedio chat then you will be able to meet doctor in the google meet ";
    }  else if (userInput.toLowerCase().includes('appointment')) {
      botReply = "you  can go through the Book Your Appointments UI then you are able to book an appointment ";
    } 
    else if (userInput.toLowerCase().includes('thank')) {
      botReply = "You're welcome! Let me know if there's anything else I can help with.";
    } else {
        botReply = "I'm sorry, I cannot process your request at the moment.";
    }
    
    appendBotMessage(botReply);
    
    // Scroll to the bottom of the chat container to show the latest message
    var chatContainer = document.querySelector('.chatbot-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
