const spinner = document.getElementById("spinner");
const codePin = document.getElementById('id_code_pin')
const countryInput = document.getElementById('id_country')
const receiverInput = document.getElementById('id_receiver')
const fromCurrencyInput = document.querySelector('#id_amount')
const toCurrencyInput = document.querySelector('#id_amount_converted')

const submitBtn = document.querySelector('#submit-btn')


countryInput.onchange = handleCountryOnChange 

fromCurrencyInput.onchange = handleChangeOnFromAmountInput
toCurrencyInput.onchange = handleChangeOnToAmountInput
codePin.addEventListener('keypress',typeOnlyDigits)

function typeOnlyDigits(e){
    if (e.which < 48 || e.which > 57) {
    e.preventDefault();
  }
}




function handleChangeOnFromAmountInput(e) {
    imposeMinMax(e.target)
}


function imposeMinMax(el){
    if(el.value != ""){
      if(parseInt(el.value) < parseInt(el.min)){
        el.value = el.min;
      }
      if(parseInt(el.value) > parseInt(el.max)){
        el.value = el.max;
      }
    }
  }



function inputsAreNotBlank(){
    return (
        countryInput.value != ' ' && 
        fromCurrencyInput.value != '' && 
        toCurrencyInput.value != '' &&
        receiverInput.value != ' ' &&
        codePin.value != ''
    )
}
function handleTransactionFormDidSubmit(e){
        e.preventDefault()
        const myForm = e.target
        const myFormData = new FormData(myForm)
        const url = myForm.getAttribute('action')
        const method = myForm.getAttribute('method')
        if (inputsAreNotBlank()){

            const xhr = new XMLHttpRequest()
            const responseType = 'json'
        xhr.responseType = responseType
        xhr.open(method, url)
        xhr.onload =  function(){
            if(xhr.status === 201){
                // console.log(xhr.response)
                // myForm.reset()
                displayMessage('Transaction has been completed', 'success')
                redirect(xhr.response.url)
            } else if(xhr.status === 400){
                const formErrors = getAllErrors(xhr.response.errors)
                displayMessage(formErrors[0], 'error')
            //    console.log(xhr.response)
            }else if (xhr.status === 500){
                alert('There was a server error, please try again.')
            }
        }
        xhr.onerror = function(){
            alert('An error occured, Please try again later.')
        }
        xhr.send(myFormData)
    }else{
        displayMessage('please fill all the fields','error')
    }
}
document.getElementById('form')
.addEventListener('submit', handleTransactionFormDidSubmit)
