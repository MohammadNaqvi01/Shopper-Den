$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



$(document).ready(function(){

    $('.plus-cart').click(function(){
        var id=$(this).attr("pid").toString();
        var eml= this.parentNode.children[2]
        alert(eml) 
        $.ajax({
            type:"GET",
            url:"/pluscart",
            data:{
                product_id:id
            },
            success:function(data){
              
              eml.innerText=data.quantity
              document.getElementById("amount").innerText=data.amount
              document.getElementById("total").innerText=data.total
              
            }
        });
    
    
    
    });
  
  });










// REDUCE NUMBER OF ITEMS
$(document).ready(function(){

    $('.minus-cart').click(function(){
        var id=$(this).attr("pid").toString();
        var eml= this.parentNode.children[2]
        var rmv=$(this).parents(".row1")
      
        alert(eml)
        $.ajax({
            type:"GET",
            url:"/minuscart",
            data:{
                product_id:id
            },
            success:function(data){
                alert(data.quantity)  
                if(data.quantity==0){
                    rmv.remove()
                    document.getElementById("amount").innerText=data.amount
                    document.getElementById("total").innerText=data.total
                  
                }
                else{

                
                eml.innerText=data.quantity
                document.getElementById("amount").innerText=data.amount
                document.getElementById("total").innerText=data.total
                }
                alert("done")
              //eml.innerText=data.quantity
            }
        });
    
    
    
    });
      
  
  });





// REMOVE CART ITEM
$(document).ready(function(){


    $('.remove-cart').click(function(){
        var id=$(this).attr("pid").toString();
        var eml=$(this).parents(".row1")
        alert(eml)
        $.ajax({
            type:"GET",
            url:"/removecart",
            data:{
                product_id:id
            },
            success:function(data){
             eml.remove()
             document.getElementById("amount").innerText=data.amount
             document.getElementById("total").innerText=data.total
       
             
            }
        });
    
    
    
    }); 
  
  });
