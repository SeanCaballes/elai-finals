$(document).ready(function() {
    $('#chatbot-toggle').click(function() {
        $('#chatbot-popup').toggle();
    });

    $('#close-chat').click(function() {
        $('#chatbot-popup').hide();
    });

    $('#send-message').click(function() {
        var userMessage = $('#user-message').val();
        if (userMessage.trim() !== '') {
            $('#chatbot-messages').append('<div class="user-message"><strong>You:</strong> ' + userMessage + '</div>');
            $('#user-message').val('');

            // Send user message to the backend for processing
            $.ajax({
                url: '/get_relevant_text',  // New endpoint to handle query
                method: 'POST',
                data: { query: userMessage },
                success: function(response) {
                    var botResponse = response.text || "I couldn't find any relevant information."; // Default message if no relevant info is found

                    // Display the bot's response
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
