function animationList(className){
    var items = document.getElementsByClassName(className)
    for(var i = 0; i < items.length; i ++){
        var item = toggleAnimation(i, items);
        setTimeout(item, i*60);
    }   
}
function toggleAnimation(i, items) {
        var animationItem = items[i];
        return function() {
            animationItem.classList.toggle('enter');
        }
} 