
const codePinToggle = document.getElementById('code-pin-toggle')
const codePinBox = document.getElementById('code-pin')
const codePinHome = codePinBox.dataset.code
codePinToggle.onclick = function(){
    if(codePinToggle.classList.contains('show')){
        codePinToggle.classList.remove('show')
        codePinBox.innerText = '* * * *'
    }else{
        codePinToggle.classList.add('show')
        codePinBox.innerText = `${codePinHome[0]} ${codePinHome[1]} ${codePinHome[2]} ${codePinHome[3]}`
    }
}
