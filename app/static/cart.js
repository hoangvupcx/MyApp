function addToCart(id, name, price, image) {
    fetch('/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "image": image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload();
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    })
}

function updateCart(productId, obj) {
    fetch(`/cart/${productId}`, {
        method: 'put',
        body: JSON.stringify ({
            'quantity': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
        let d2 = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString('en-US')
    }).catch(err => console.error(err))
}


function deleteCart(productId) {
    if(confirm('Are you sure to delete this product?') == true) {
        fetch(`/cart/${productId}`, {
            method: 'delete'
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString('en-US')

        let r = document.getElementById(`cart${productId}`)
        r.style.display ='none'
    }).catch(err => console.error(err))
    }
}

function pay() {
    if (confirm("Do you want to pay all?") == true) {
        fetch("/pay", {
             method: 'post',
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => {
            console.info(res)
            return res.json()
        }).then(data => {
            alert(data.message);
            location.reload()
        }).catch(err => {
            console.error(err)
        })
    }
}

function deleteAll()  {
    if (confirm("Do you want to delete all?") == true) {
        fetch("/delete", {
        headers: {
            'Content-Type': 'application/json'
        }
        }).then(res => {
            console.info(res)
            return res.json()
        }).then(data => {
            alert(data.message);
            location.reload()
        }).catch(err => {
            console.error(err)
        })
    }
}
