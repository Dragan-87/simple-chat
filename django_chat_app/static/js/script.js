function clearForm() {
  document.getElementById('username').value = '';
  document.getElementById('first_name').value = '';
  document.getElementById('last_name').value = '';
  document.getElementById('email').value = '';
  document.getElementById('password').value = '';
}

function checkPasswordMatch() {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;
  if (password != confirmPassword) {
    document.getElementById('registerButton').disabled = true;
    return false;
  }
  document.getElementById('registerButton').disabled = false;
  return true;
}
