var createAccountForm = document.getElementById('create_account_form')
var loginForm = document.getElementById('login_form')

function showCreateForm(){
   createAccountForm.classList.remove('hidden');
   loginForm.classList.add('hidden');
}

function showLoginForm(){
   createAccountForm.classList.add('hidden');
   loginForm.classList.remove('hidden');
}
