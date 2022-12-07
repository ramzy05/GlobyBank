const codePin = document.getElementById('id_code_pin');
const currencyInput = document.querySelector('#id_amount');

const submitBtn = document.querySelector('#submit-btn');

currencyInput.onchange = handleChangeOnAmountInput;
codePin.addEventListener('keypress', typeOnlyDigits);

function inputsAreNotBlank() {
	return currencyInput.value != '' && codePin.value != '';
}

function handleTransactionFormDidSubmit(e) {
	e.preventDefault();
	spinner.removeAttribute('hidden');
	const myForm = e.target;
	const myFormData = new FormData(myForm);
	myFormData.append('action', e.target.dataset.action);

	const url = myForm.getAttribute('action');
	const method = myForm.getAttribute('method');
	if (inputsAreNotBlank()) {
		const xhr = new XMLHttpRequest();
		const responseType = 'json';
		xhr.responseType = responseType;
		xhr.open(method, url);
		xhr.onload = function () {
			spinner.setAttribute('hidden', false);

			if (xhr.status === 201) {
				// console.log(xhr.response)
				// myForm.reset()
				displayMessage(xhr.response.message, 'success');
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
		spinner.setAttribute('hidden', false);
		displayMessage('please fill all the fields', 'error');
	}
}
document
	.getElementById('form')
	.addEventListener('submit', handleTransactionFormDidSubmit);
