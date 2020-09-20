
/*
function to show the notification system.
:param `response` is message text to display.
:param `className` is class message, e.g: 'success', 'warning', 'error'
*/
var showNotif = function(response, className, doReload, position) {
  var position = position || 'top center';
  $.notify(response, {
    globalPosition: position,
    className: className
  });
  if(doReload == true) {
    setTimeout(function(){
      location.reload();
    }, 3000);
  }
}


/*
function to change the base url of paginator, e.g:
/posts/list/?page=1&q=a   =>   /posts/me/?page=1&q=a
:param `url` is base url changer, e.g: /posts/me/
:param `element` is string id/class element.
*/
var changeBaseURLPaginator = function(url, element) {
  var elementMain = element || '.main-pagination';
  if(typeof(elementMain) == 'object') {elementMain = element} else {elementMain = $(element)}

  var elementMain = $(element);
  elementMain.find('a.page-link').each(function() {
    var item = $(this);
    if(item.attr('href') != 'undefined') {
      var itemURL = item.attr('href') || '';
      var itemURLSplit = itemURL.split('?');
      var gotoURL = url;

      if(itemURLSplit.length > 1) {
        gotoURL = url + '?' + itemURLSplit[1];
      }
      item.attr({'href': gotoURL});
    }
  });

  // change action form go to page
  elementMain.find('.form-go-to-page')
         .attr({'action': url});
}
