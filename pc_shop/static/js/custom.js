// function ajaxSend(url, params) {
//     // Отправляем запрос
//     fetch(`${url}?${params}`, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//     })
//         .then(response => response.json())
//         .then(json => render(json))
//         .catch(error => console.error(error))
// }

const forms = document.querySelector('form[name=btn_add_to_cart]')
forms.addEventListener('submit',  event => {
    event.preventDefault();
    let url = '/add_cart'
    let params = Object.fromEntries(new FormData(forms))["product_id"];
    let cookie = document.cookie;
    fetch(`${url}/${params}/`, {
        method: 'GET',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        cookie: cookie
    })
})


let myToast1 = document.getElementById('myToast1')
let showToast = () => {
    window.scrollTo(pageYOffset, 0);
    bootstrap.Toast.getOrCreateInstance(myToast1).show();
}

// border: 3px solid red