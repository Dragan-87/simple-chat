function chatStringHTMLTemplate(username, chatMsg) {
  return ` <div id="deleteMsg"><span class="mr-8 gray">${new Date().toLocaleDateString(
    'en-US',
    { month: 'short', day: 'numeric', year: 'numeric' }
  )}</span> <b>${username.value}</b>: <span class="gray">${chatMsg.value
    }</span></div>`;
}

function setChatStringWithJson(data) {
  return ` <div><span class="mr-8 gray">${formatDate(
    data.fields.created_at
  )}</span> <b>${data.fields.author}</b>: ${data.fields.text}</div>`;
}

/**
 * Clears the form by resetting the values of the input fields.
 */
function clearForm() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
}

/**
 * Clears the registration form by resetting the values of all input fields.
 */
function clearRegisterFrom() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
  document.getElementById('password').value = '';
  document.getElementById('confirm_password').value = '';
}

function loginFormData() {
  let form = new FormData();
  let token = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  form.append('username', username.value);
  form.append('password', password.value);
  form.append('csrfmiddlewaretoken', token);
  return form
}

/**
 * Checks if the password and confirm password fields match, and if all required fields are filled.
 * @returns {boolean} Returns true if the password and confirm password fields match and all required fields are filled, otherwise returns false.
 */
function checkPasswordMatch() {
  registerButton.disabled = true;
  if (
    password.value.trim() != confirm_password.value.trim() ||
    !username.value.trim() ||
    !email.value.trim() ||
    !first_name.value.trim() ||
    !last_name.value.trim() ||
    !password.value.trim() ||
    !confirm_password.value.trim()
  ) {
    registerButton.disabled = true;
    return false;
  }
  registerButton.disabled = false;
  return true;
}

/**
 * Checks if the message text is empty.
 *
 * @returns {boolean} Returns true if the message text is not empty, otherwise false.
 */
function isMessageTextEmpty() {
  if (!chatMsg.value.trim()) {
    document.getElementById('sendButton').disabled = true;
    return false;
  }
  document.getElementById('sendButton').disabled = false;
  return true;
}

/**
 * Creates a new FormData object and sets the necessary form data.
 * @returns {FormData} The FormData object with the form data set.
 */
function setAllFormData() {
  let form = new FormData();
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form.append('textmessage', chatMsg.value);
  form.append('csrfmiddlewaretoken', token);
  chatMsg.value = '';
  token = '';
  return form;
}

/**
 * Formats a given date into a string representation.
 *
 * @param {Date} date - The date to be formatted.
 * @returns {string} The formatted date string.
 */
function formatDate(date) {
  const d = new Date(date);
  const monthName = d.toLocaleString('de-DE', { month: 'short' }).split(' ')[0];
  const day = d.getDate();
  const year = d.getFullYear();

  const formattedDate = `${monthName}. ${day}, ${year}`;
  return formattedDate;
}

/**
 * Handles errors during registration.
 *
 * @param {Object} data - The error data.
 */
function handleRegisterErrors(data) {
  if (data.fields && data.fields.wrong_password) {
    messageContainer.innerHTML = '';
    messageContainer.innerHTML += requestHTMLTemplate(
      data.fields.wrong_password
    );
    setTimeout(() => {
      messageContainer.innerHTML = '';
    }, 2000);
    return;
  }

  if (data.fields && data.fields.user_exists) {
    messageContainer.innerHTML = '';
    messageContainer.innerHTML += requestHTMLTemplate(data.fields.user_exists);
    setTimeout(() => {
      messageContainer.innerHTML = '';
    }, 2000);
    return;
  }
}

/**
 * Handles the successful registration of a user.
 *
 * @param {Object} data - The data returned from the registration request.
 */
function handleSuccessfulyRegister(data) {
  if (data.fields && data.fields.username) {
    messageContainer.innerHTML = '';
    messageContainer.innerHTML += requestHTMLTemplate(data.fields.username);
    setTimeout(() => {
      window.location.href = '/login/';
    }, 1000);
  }
}

/**
 * Generates an HTML template with a container div that slides in from the left.
 *
 * @param {string} data - The HTML content to be inserted into the template.
 * @returns {string} The generated HTML template.
 */
function requestHTMLTemplate(data) {
  return `<div class="container slideInFromLeft">${data}</div>`;
}

/**
 * Creates a FormData object with the values from the registration form.
 * @returns {FormData} The FormData object containing the form data.
 */
function setRegisterFormData() {
  let form = new FormData();
  form.append('username', document.getElementById('username').value.trim());
  form.append('first_name', document.getElementById('first_name').value.trim());
  form.append('last_name', document.getElementById('last_name').value.trim());
  form.append('email', document.getElementById('email').value.trim());
  form.append('password', document.getElementById('password').value.trim());
  form.append(
    'confirm_password',
    document.getElementById('confirm_password').value.trim()
  );
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form.append('csrfmiddlewaretoken', token);
  return form;
}

/**
 * Performs a logout operation.
 * @async
 * @function logout
 * @returns {Promise<void>} - A promise that resolves when the logout operation is completed.
 */
async function logout() {
  let form = new FormData();
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form.append('csrfmiddlewaretoken', token);

  let requestOptions = {
    method: 'POST',
    body: form,
  };

  try {
    const response = await fetch('/logout/', requestOptions);
    const data = await response.json();

    if (data.fields.logout) {
      window.location.href = '/login/';
    } else {
      console.error('Logout failed');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

/**
 * Sends a message to the server and updates the message container with the response.
 * @async
 * @function sendMessage
 * @returns {Promise<void>} A promise that resolves when the message is sent and the message container is updated.
 * @throws {Error} If there is an error during the message sending process.
 */
async function sendMessage() {
  let form = setAllFormData();
  let requestOptions = {
    method: 'POST',
    body: form,
  };

  msgContainer.innerHTML += chatStringHTMLTemplate(username, chatMsg);

  try {
    const request = await fetch('/chat/', requestOptions);
    const response = await request.json();
    const data = await JSON.parse(response);
    deleteMsg.remove();
    msgContainer.innerHTML += setChatStringWithJson(data)
  } catch (error) {
    console.error('Error:', error);
  }
}

/**
 * Performs a login request using the provided username and password.
 *
 * @async
 * @function login
 * @returns {Promise<void>} A promise that resolves when the login request is completed.
 * @throws {Error} If an error occurs during the login request.
 */
async function login() {
  let form = loginFormData()

  let requestOptions = {
    method: 'POST',
    body: form,
  };

  try {
    request = await fetch('/login/', requestOptions);
    data = await request.json();

    if (data.fields && data.fields.username) {
      document.getElementById('loginContainer').innerHTML +=
        requestHTMLTemplate(data.fields.username);
      setTimeout(() => {
        window.location.href = '/chat/';
      }, 500);
    }

    if (data.fields && data.fields.wrong_password) {
      loginContainer.innerHTML += requestHTMLTemplate(
        data.fields.wrong_password
      );
      setTimeout(() => {
        loginContainer.innerHTML = '';
      }, 1000);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

/**
 * Registers a user by sending a POST request to the '/register/' endpoint.
 *
 * @async
 * @function register
 * @returns {Promise<void>} A promise that resolves when the registration is complete.
 */
async function register() {
  let formData = setRegisterFormData();
  clearRegisterFrom();
  let requestOptions = {
    method: 'POST',
    body: formData,
  };

  try {
    const response = await fetch('/register/', requestOptions);
    const data = await response.json();

    handleSuccessfulyRegister(data);

    handleRegisterErrors(data);
  } catch (e) {
    console.log(e);
  }
}

function toLoginPage() {
  window.location.href = '/login/';
}

function toggleLoginButton() {
  
  if (username.value.trim() && password.value.trim()) {
    loginButton.disabled = false;
    return;
  }
  loginButton.disabled = true;
}
