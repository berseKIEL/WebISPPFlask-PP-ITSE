let previousFila;
$(document).ready(function(){
    $('.fila').click(function(){
        $(previousFila).css('background-color', '');
        $(previousFila).css('color', 'black');
        $(this).css('background-color', 'rgb(101, 105, 110)');
        $(this).css('color', 'white');
        previousFila = this
    })
    $('.fila').dblclick(function(){
        var idtr = $(this).attr('id');
        document.getElementById('idplan').value = idtr;
        document.getElementById("mostrar-materia").submit();
    })
})