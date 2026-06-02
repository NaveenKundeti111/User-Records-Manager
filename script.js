const API_BASE = "http://127.0.0.1:5000/api";
const userTable = document.getElementById("userTable");
const recommendationText = document.getElementById("recommendationText");
const themeNameEl = document.getElementById("themeName");
const themeDetailsEl = document.getElementById("themeDetails");

window.addEventListener("DOMContentLoaded", getUsers);

async function getUsers() {
    try {
        const response = await fetch(`${API_BASE}/users`);
        if (!response.ok) throw new Error(`Unable to load users: ${response.status}`);
        const users = await response.json();
        userTable.innerHTML = users.map(buildRow).join("");
    } catch (error) {
        console.error(error);
        userTable.innerHTML = `<tr><td colspan="4">Unable to load users. Start the Python backend and reload.</td></tr>`;
    }
}

function buildRow(user) {
    return `
        <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.age !== undefined ? user.age : "—"}</td>
            <td>
                <button onclick="updateUser(${user.id})">Edit</button>
                <button onclick="deleteUser(${user.id})">Delete</button>
            </td>
        </tr>`;
}

async function createUser() {
    const nameInput = document.getElementById("name");
    const ageInput = document.getElementById("age");
    const name = nameInput.value.trim();
    const age = parseInt(ageInput.value, 10);

    if (!name) {
        alert("Please enter a name before saving.");
        return;
    }
    if (Number.isNaN(age) || age <= 0) {
        alert("Please enter a valid age greater than zero.");
        return;
    }

    try {
        const themeResponse = await fetch(`${API_BASE}/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, age })
        });

        if (!themeResponse.ok) throw new Error(`Recommendation failed: ${themeResponse.status}`);
        const theme = await themeResponse.json();
        displayRecommendation(theme);

        const response = await fetch(`${API_BASE}/users`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, age })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed to save user: ${response.status} ${errorText}`);
        }

        nameInput.value = "";
        ageInput.value = "";
        getUsers();
    } catch (error) {
        console.error(error);
        alert(`Unable to save user: ${error.message}`);
    }
}

function displayRecommendation(theme) {
    recommendationText.textContent = `The ML model recommends ${theme.theme} style for a ${theme.age} year old. This palette uses ${theme.style} energy.`;
    themeNameEl.textContent = theme.theme;
    themeNameEl.style.background = theme.accent;
    themeNameEl.style.color = theme.textColor;
    themeDetailsEl.innerHTML = `
        <p><strong>Accent color:</strong> ${theme.accent}</p>
        <p><strong>Background style:</strong> ${theme.background}</p>
    `;
}

async function updateUser(id) {
    const newName = prompt("Enter new name:");
    if (newName === null) return;
    const trimmedName = newName.trim();
    if (!trimmedName) {
        alert("Name cannot be empty.");
        return;
    }

    const newAgeString = prompt("Enter new age:");
    if (newAgeString === null) return;
    const newAge = parseInt(newAgeString, 10);
    if (Number.isNaN(newAge) || newAge <= 0) {
        alert("Please enter a valid age greater than zero.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: trimmedName, age: newAge })
        });

        if (!response.ok) throw new Error(`Update failed: ${response.status}`);
        getUsers();
    } catch (error) {
        console.error(error);
        alert("Unable to update user. Please try again.");
    }
}

async function deleteUser(id) {
    if (!confirm("Delete this user permanently?")) return;

    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error(`Delete failed: ${response.status}`);
        getUsers();
    } catch (error) {
        console.error(error);
        alert("Unable to delete user. Please try again.");
    }
}
