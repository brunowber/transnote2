  $(document).ready(function(){
    $('.ui.sticky').sticky({
        context: '#main'
      });
    $('.sobre').click(function(){
      alert('oi');
      $('.dimmer').dimmer('show');

    })
      var path = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
      $('select[name=uf]').on('change', function() {

        $.ajax({
            url: path + "/get-cidades/", // url
            type: 'POST',
            dataType: 'json',
            data: {uf: $(this).val()},
            beforeSend: function () {
                $("select[name=cidade]").html("<option value=''>Carregando...</option>");
            },
            success: function (data, textStatus, xhr) {
                var html = null;
                var cidade = data;

                $(cidade).each(function (key, val) {
                    html += '<option value="' + val.pk + '">' + val['fields']['nome'] + '</option>';
                });
                $('select[name=cidade]').html(html);

            },
            error: function (xhr, textStatus, errorThrown) {
                $('select[name=cidade]').html('<option value="">Nenhuma cidade cadastrada para este estado</option>');
            }
        });
    });

      $('.paineis .item').click(function(){
      idI= $(this).contents().filter(function() {
          return this.nodeType === 1;
        }).filter('i').attr('id')

      i = $('#'+idI)

          if ($(i).hasClass('add')){
              
              $(i).removeClass('add').addClass('minus')
              id = $(i).attr('id')

              $('.'+id).show()
              
           }
           else if ($(i).hasClass('minus')){
              id = $(i).attr('id')
              $(i).removeClass('minus').addClass('add')
              
              $('.'+id).hide()
           }
      })


    $('#busca').change(function(){

      $('.escondidos .field').css('display', 'none')
      $('.escondidos .field input').attr('name', '')
      busca = $('#busca option:selected').attr('id')
      
      $('.'+busca).toggle()
      $('.'+busca+' input').attr('name', 'param1')

    })


    $('.fazul').click(function(){
        
        id = $(this).attr('id')
        $('.'+id).transition('slide down')
    })

    $('.cazul').click(function(){
        
        id = $(this).attr('id')
        $('.'+id).transition('slide down')
    })

  })