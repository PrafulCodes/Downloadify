document.getElementById('feedback-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const subject = document.getElementById('subject').value.trim();
    const comments = document.getElementById('comments').value.trim();

    // Prepare EmailJS parameters
    const params = {
        from_name: name,
        from_email: email,
        subject: subject,
        comments: comments,
        to_name: 'Admin'
    };

    // Basic validation
    if (name && email && subject && comments) {
        emailjs.send('service_r55to0f', 'template_uvnqch8', params)
        .then(() => {
            alert('Thank you for your message!');
            document.getElementById('feedback-form').reset();
        }, (error) => {
            alert('Failed to send message. Please try again later.');
            console.error('EmailJS Error:', error);
        });
    } else {
        alert('Please fill in all fields before submitting.');
    }
});
