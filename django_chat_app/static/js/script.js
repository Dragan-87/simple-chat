allMessages = [];

function clearForm() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
}

function checkPasswordMatch() {
  const username = username.value;
  const email = email.value;
  const first_name = first_name.value;
  const last_name = last_name.value;
  const password = password.value;
  const confirmPassword = confirmPassword.value;
  if (password != confirmPassword || !username || !email || !first_name || !last_name || !password) {
    document.getElementById('registerButton').disabled = true;
    return false;
  }
  document.getElementById('registerButton').disabled = false;
  return true;
}

function isMessageTextEmpty() {
  const chatMsg = document.getElementById('chatMsg').value;
  if (chatMsg === '') {
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

    msgContainer.innerHTML += ` <div><span class="mr-8 gray">${new Date(
      data.fields.created_at
    ).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })}</span> <b>${data.fields.author}</b>: ${data.fields.text}</div>`;
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
