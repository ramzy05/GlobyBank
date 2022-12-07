const spinner = document.getElementById('spinner');
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
function redirect(url) {
	setTimeout(() => {
		window.location.href = url;
	}, 1700);
	//hidde message occurs after 1500ms
	return;
}
function imposeMinMax(el) {
	if (el.value != '') {
		if (parseInt(el.value) < parseInt(el.min)) {
			el.value = el.min;
		}
		if (parseInt(el.value) > parseInt(el.max)) {
			el.value = el.max;
		}
	}
}

function handleChangeOnAmountInput(e) {
	imposeMinMax(e.target);
}
function typeOnlyDigits(e) {
	if (e.which < 48 || e.which > 57) {
		e.preventDefault();
	}
}
