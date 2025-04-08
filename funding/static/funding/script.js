document.querySelector(".btn-danger").addEventListener("click", function (event) {
    // Prevent the default action
    event.preventDefault();

    // Show the confirmation modal
    const modal = document.querySelector("#confirmationModal");
    modal.style.display = "block";

    // Handle the confirm button
    document.querySelector("#confirmDelete").addEventListener("click", function () {
        modal.style.display = "none";

        // Send a POST request to delete the account
        fetch('/delete_account/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                console.log("Account deleted successfully");
                // Redirect to a different page (e.g., home or login)
                window.location.href = '/login/';
            } else {
                console.error("Failed to delete account");
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Handle the cancel button
    document.querySelector("#cancelDelete").addEventListener("click", function () {
        modal.style.display = "none";
        console.log("Delete canceled");
    });
});

