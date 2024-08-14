allMessages = [];

function clearForm() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
}

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

function isMessageTextEmpty() {
  if (!chatMsg.value.trim()) {
    document.getElementById('sendButton').disabled = true;
    return false;
  }
  document.getElementById('sendButton').disabled = false;
  return true;
}

function setAllFormData() {
  let form = new FormData();
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form.append('textmessage', chatMsg.value);
  form.append('csrfmiddlewaretoken', token);
  chatMsg.value = '';
  token = '';
  return form;
}

async function sendMessage() {
  let form = setAllFormData();
  let requestOptions = {
    method: 'POST',
    body: form,
  };

  msgContainer.innerHTML += ` <div id="deleteMsg"><span class="mr-8 gray">${new Date().toLocaleDateString(
    'en-US',
    { month: 'short', day: 'numeric', year: 'numeric' }
  )}</span> <b>${username.value}</b>: <span class="gray">${
    chatMsg.value
  }</span></div>`;

  try {
    const request = await fetch('/chat/', requestOptions);
    const response = await request.json();
    const data = await JSON.parse(response);
    deleteMsg.remove();

    msgContainer.innerHTML += ` <div><span class="mr-8 gray">${formatDate(
      data.fields.created_at
    )}</span> <b>${data.fields.author}</b>: ${data.fields.text}</div>`;
  } catch (error) {
    console.error('Error:', error);
  }
}

async function loadMessagesFromServer() {
  try {
    const request = await fetch('/chat/');
    const response = await request.json();
    const data = await JSON.parse(response);
  } catch (error) {
    console.error('Error:', error);
  }
}

function formatDate(date) {
  const d = new Date(date);
  const monthName = d.toLocaleString('de-DE', { month: 'short' }).split(' ')[0];
  const day = d.getDate();
  const year = d.getFullYear();

  const formattedDate = `${monthName}. ${day}, ${year}`;
  return formattedDate;
}

async function login() {
  let form = new FormData();
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  form.append('username', username.value);
  form.append('password', password.value);
  form.append('csrfmiddlewaretoken', token);

  let requestOptions = {
    method: 'POST',
    body: form,
  };

  try {
    request = await fetch('/login/', requestOptions);
    data = await request.json();

    document.getElementById('loginContainer').innerHTML +=
      loginSuccessHtmlTemplate(data);
    setTimeout(() => {
      window.location.href = '/chat/';
    }, 500);
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

function handleSuccessfulyRegister(data) {
  if (data.fields && data.fields.username) {
    messageContainer.innerHTML = '';
    messageContainer.innerHTML += requestHTMLTemplate(data.fields.username);
    setTimeout(() => {
      window.location.href = '/login/';
    }, 1000);
  }
}

function requestHTMLTemplate(data) {
  return `<div class="container slideInFromLeft">${data}</div>`;
}

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

function clearRegisterFrom() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
  document.getElementById('password').value = '';
  document.getElementById('confirm_password').value = '';
}
