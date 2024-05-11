var updateBts = document. getElementsByClassName ('update-cart')

for (i = 0; i < updateBts.length; i++) 
{
    updateBts [i].addEventListener ('click', function (){
        var productId = this.dataset.product
        var action = this. dataset. action
        console. Log('productId:', productId, 'Action:', action)
        })
}