document.addEventListener('DOMContentLoaded', () => {
    const userList = document.getElementById('user-list');

    // Fetch data from our own backend server
            fetch('/api/data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(users => {
            if (!Array.isArray(users)) {
                throw new Error('Data is not an array');
            }
            // Clear the 'Loading...' message
            userList.innerHTML = '';

            // Loop through each user and create a list item
            users.forEach(user => {
                const listItem = document.createElement('li');
                listItem.textContent = `${user.name} - ${user.email}`;
                userList.appendChild(listItem);
            });
        })
        .catch(error => {
            userList.innerHTML = `<li style="color: red;">Failed to load data: ${error.message}</li>`;
            console.error('Fetch error:', error);
        });
});
