$(document).ready(function() {
    var
      $userDropdown = $('.user.dropdown'),
      $addDropdown  = $('.add.dropdown'),
      $button       = $('.ui.button'),
      $watchButton  = $('.watch.button'),
      $search       = $('.page.header input'),
      $popup        = $('[data-content]'),
      $checkbox     = $('.ui.checkbox')
    ;

    $.fn.dropdown.settings.onShow = function() {
      $('body').popup('hide all');
    };

    $popup.popup({
      duration : 0,
      delay    : {
        show : 10,
        hide : 0
      },
      variation : 'inverted',
      position  : 'bottom center'
    });

    $addDropdown.dropdown({
      duration   : 0,
      action     : 'hide'
    });

    $userDropdown.dropdown({
      duration   : 0,
      transition : 'drop',
      action     : 'hide'
    });

    $watchButton.dropdown({
      allowTab: false,
      transition: 'scale',
      onChange: function(value) {
        console.log('New watch value', value);
      }
    });

    $checkbox.checkbox();

    // Focus wrapper
    $search.on('focus', function() {
      $(this).closest('.input').addClass('focused');
    })
    .on('blur', function() {
      $(this).closest('.input').removeClass('focused');
    });

    // Close a message
    $('.message .close').on('click', function() {
      $(this).closest('.message').hide();
      $('.main-messages').css({'padding': 0, 'border-bottom': 'none'});
    });
    setTimeout(function(){
      $('.main-messages').find('.message .close').trigger('click');
    }, 5000);
});
