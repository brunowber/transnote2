  $(document).ready(function(){
              
    $('#li-1').removeClass('escondida')
    $('#coluna-li-1').removeClass('escondida')
    
    $('.comandos').click(function(){
        if ($(this).hasClass('menos')){
            id = divideId(this, '-', 1)
            $('#li-'+id).addClass('escondida')
            $(this).addClass('mais').removeClass('menos').text('MAIS')
            if ($(this).hasClass('coluna')){
                id = divideId(this, '-', 2)
                $('#coluna-li-'+id).addClass('escondida')
                $(this).addClass('mais').removeClass('menos').text('MAIS')
            }
        }
        else{
            id = divideId(this, '-', 1) +1
            $('#li-'+id).removeClass()
            $(this).addClass('menos').removeClass('mais').text('MENOS')
            if ($(this).hasClass('coluna')){
                id = divideId(this, '-', 2) +1
                $('#coluna-li-'+id).removeClass()
                $(this).addClass('menos').removeClass('mais').text('MENOS')
                }
            }
    })
    
    $('.coluna').click(function(){
        if ($(this).hasClass('menos')){
            id = divideId(this, '-', 2)
            $('#coluna-li-'+id).addClass('escondida')
            $(this).addClass('mais').removeClass('menos').text('MAIS')
        }
        else{
            i=0
            $('#sortable li').each(function(){
                if (i==0)
                    if ($(this).hasClass('escondida')){
                        i=1
                        id= divideId(this, '-', 2)
                    }
            })
            $('#coluna-li-'+id).removeClass('escondida')
            $('#comandos-mais-'+id).addClass('menos').removeClass('mais').text('MENOS')
        }
    })
    
    $('.retira').click(function(){
        id=divideId(this, '-', 1)
        $('#coluna-li-'+id).addClass('escondida')
        $('#coluna-li-'+id+' select option.selecione').attr('selected','selected');    
        
        })
            
            
            

})

// $(function() {
//     $( "#sortable" ).sortable();
//     $( "#sortable" ).disableSelection();
//   });
// function divideId(obj, split, posicao){
//     id=$(obj).attr('id')
//     idSplit=id.split(split)
//     idFim=parseInt(idSplit[posicao])
//     return idFim
//     }
