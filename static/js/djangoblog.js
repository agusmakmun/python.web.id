
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
