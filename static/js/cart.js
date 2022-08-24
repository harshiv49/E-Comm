// console.log("Hello World")
var updateBtns=document.getElementsByClassName('update-cart')
function getCookies(name){
    
    
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim(); 
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        
    }
    return cookieValue;  
}
var csrftoken = getCookies('csrftoken'); 
for(i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function() {
        // product and action are the name we gave to our attributes this is similar to python self 

        var productId=this.dataset.product
        var action=this.dataset.action


        console.log("ProductId:",productId,"Action:",action)
        // apparently we inherit this from our html file
        
        
        if(user == "AnonymousUser" )
        {
            addCookieItem(productId,action)
        }
        else{
            // console.log('User Logged in ,sending data ...')
            updateUserOrder(productId,action)
        }
            
     
       
    })
   
    

}



function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	else if (action == 'remove'){
        // for some screwed reason this thing is being executed twice hence the 0.5
		cart[productId]['quantity'] =cart[productId]['quantity'] - 0.5

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	console.log('CART:', cart)
	location.reload()
}



function updateUserOrder(productId,action){
    console.log('User Logged in ,sending data ')

    var url='/update_item/'

    // when we click the damn button we go to this url and give it some post data but simultaenously dajngo routes rae triggered for url '/update-item/' which leads us to the function in views.py
//we send post data with fetch we have to provide it the url we are sending the data to

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId':productId,'action':action,
        })
    })
    .then((response)=>{
        return response.json()
    })
    .then(data=>{
        console.log('data:',data)
// location.reload()
    })
    
} 
