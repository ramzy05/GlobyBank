const receiverInput = document.getElementById('id_receiver');

function inputsAreNotBlank() {
	return (
		currencyInput.value != '' &&
		receiverInput.value != ' ' &&
		codePin.value != ''
	);
}
function handleTransactionFormDidSubmit(e) {
	e.preventDefault();
	const myForm = e.target;
	const myFormData = new FormData(myForm);
	const url = myForm.getAttribute('action');
	const method = myForm.getAttribute('method');
	if (inputsAreNotBlank()) {
		const xhr = new XMLHttpRequest();
		const responseType = 'json';
		xhr.responseType = responseType;
		xhr.open(method, url);
		xhr.onload = function () {
			if (xhr.status === 201) {
				// console.log(xhr.response)
				// myForm.reset()
				displayMessage('Transaction has been completed', 'success');
				redirect(xhr.response.url);
			} else if (xhr.status === 400) {
				const formErrors = getAllErrors(xhr.response.errors);
				displayMessage(formErrors[0], 'error');
				//    console.log(xhr.response)
			} else if (xhr.status === 500) {
				alert('There was a server error, please try again.');
			}
		};
		xhr.onerror = function () {
			alert('An error occured, Please try again later.');
		};
		xhr.send(myFormData);
	} else {
		displayMessage('please fill all the fields', 'error');
	}
}
const transacForm = document.getElementById('form');
transacForm.addEventListener('submit', handleTransactionFormDidSubmit);
