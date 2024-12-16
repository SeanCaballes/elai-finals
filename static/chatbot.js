$(document).ready(function() {
    // Toggle the chatbot popup when clicking on the button
    $('#chatbot-toggle').click(function() {
        $('#chatbot-popup').toggle();
    });

    // Close the chatbot popup when clicking on the close button
    $('#close-chat').click(function() {
        $('#chatbot-popup').hide();
    });

    // Handle sending user messages to the backend
    $('#send-message').click(function() {
        var userMessage = $('#user-message').val();
        if (userMessage.trim() !== '') {
            // Display user message
            $('#chatbot-messages').append('<div class="user-message"><strong>You:</strong> ' + userMessage + '</div>');
            $('#user-message').val('');

            // Send user message to the Flask backend (Gemini API)
            $.ajax({
                url: '/get_relevant_text',  // Flask route
                method: 'POST',
                data: { query: userMessage },  // Send the user message to the backend
                success: function(response) {
                    if (response.status === 'success' && response.results) {
                        var botResponse = response.results.join('<br/>');
                    } else {
                        var botResponse = response.text || "I couldn't find anything related to your query.";
                    }

                    // Display bot response
                    $('#chatbot-messages').append('<div class="bot-message"><strong>Bot:</strong> ' + botResponse + '</div>');
                    $('#chatbot-messages').scrollTop($('#chatbot-messages')[0].scrollHeight);
                },
                error: function() {
                    $('#chatbot-messages').append('<div class="bot-message"><strong>Bot:</strong> Sorry, there was an error processing your request.</div>');
                }
            });
        }
    });
});
