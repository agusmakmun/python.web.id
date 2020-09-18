// highlight pre
$('.martor-preview pre').each(function(i, block){
  hljs.highlightBlock(block)
});

var showNotif = function(response, className, doReload) {
  $.notify(response, {
    globalPosition: 'top center',
    className: className
  });
  if(doReload == true) {
    setTimeout(function(){
      location.reload();
    }, 3000);
  }
}

// vote up and vote down
$(document).on('click', '.vote-up, .vote-down', function() {
  var voteUrl = $(this).data('target');

  $.ajax({
      url: voteUrl,
      type: 'GET',
      success: function(response) {
        showNotif(response, 'success', true);
      },
      error: function(xhr, options, response) {
        showNotif(response, 'error', false);
      }
  });
});

// undo vote up and vote down
$(document).on('click', '.undo-vote-up, .undo-vote-down', function() {
  var undoVoteUrl = $(this).data('target');
  $.ajax({
      url: undoVoteUrl,
      type: 'GET',
      success: function(response) {
        if(response['success']) {
          showNotif(response['message'], 'success', true);
        }else {
          showNotif(response['message'], 'warn', false);
        }
      },
      error: function(xhr, options, response) {
        console.log(xhr, options, response);
        showNotif(response, 'error', false);
      }
  });
});

// view upvote and downvote totals
$(document).on('click', '.vote-total-public-value', function() {
  $(this).closest('.vote-total').find('.vote-total-hidden-value').show();
  $(this).hide();
});

// bookmark action
$(document).on('click', '.favorite-icon', function() {
  var favoriteUrl = $(this).data('target');
  $.ajax({
      url: favoriteUrl,
      type: 'GET',
      success: function(response) {
        if(response['success']) {
          showNotif(response['message'], 'success', true);
        }else {
          showNotif(response['message'], 'warn', false);
        }
      },
      error: function(xhr, options, response) {
        showNotif(response, 'error', false);
      }
  });
});

// mark as featured or remove from featured
$(document).on('click', '.mark-as-featured', function() {
  var featuredUrl = $(this).data('target');
  var mode = $(this).data('mode');
  $.ajax({
      url: featuredUrl+'?mode='+mode,
      type: 'GET',
      success: function(response) {
        if(response['success']) {
          showNotif(response['message'], 'success', true);
        }else {
          showNotif(response['message'], 'warn', false);
        }
      },
      error: function(xhr, options, response) {
        showNotif(response, 'error', false);
      }
  });
});

// dropdown share
$(document).on('click', '.button-copy-link-post', function(e) {
  e.preventDefault(); // stop triggering the form
  $('.input-link-post').select();
  document.execCommand('copy');
  let message = $(this).data('success-message');
  showNotif(message, 'success', false);
});

// delete post action
$(document).on('click', '.delete-action', function() {
  var postDeletUrl = $(this).data('target');
  var confirmMessage = $(this).data('confirm-message');

  $.notify.addStyle('foo', {
    html:
      "<div>" +
        "<div class='clearfix'>" +
          "<div class='title' data-notify-html='title'/>" +
          "<div class='buttons'>" +
            "<button class='ui mini button red yes' data-notify-text='button'></button>" +
            "<button class='ui mini button no'>Cancel</button>" +
          "</div>" +
        "</div>" +
      "</div>"
  });
  $(document).on('click', '.notifyjs-foo-base .no', function() {
    $(this).trigger('notify-hide');
  });
  $(document).on('click', '.notifyjs-foo-base .yes', function() {
    $.ajax({
        url: postDeletUrl,
        type: 'GET',
        success: function(response) {
          if(response['success']) {
            showNotif(response['message'], 'success', true);
            window.location = '/';
          }else {
            showNotif(response['message'], 'warn', false);
          }
        },
        error: function(xhr, options, response) {
          showNotif(response, 'error', false);
        }
    });
    $(this).trigger('notify-hide');
  });

  $.notify({
    title: confirmMessage,
    button: 'Confirm'
  }, {
    style: 'foo',
    //autoHide: false,
    globalPosition: 'top center',
    clickToHide: false
  });
});
