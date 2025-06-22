const registerForm = document.getElementById('registerForm');
const loginForm = document.getElementById('loginForm');

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(registerForm);
  const data = Object.fromEntries(formData);

  const res = await fetch('http://localhost:5000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  alert(result.message);
});

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(loginForm);
  const data = Object.fromEntries(formData);

  const res = await fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await res.json();
  if (result.user_id) {
    alert("Login successful! User ID: " + result.user_id);
  } else {
    alert(result.error);
  }
});
