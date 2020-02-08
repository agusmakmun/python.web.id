(function ($) {
  /*****
  semantic calendar widget
  require `semantic.min.js` and `semantic-calendar.min.js`

  html structure:

  <div class="field">
    <label>Birth date</label>
    <div class="ui calendar">
      <div class="ui input left icon">
        <i class="calendar icon"></i>
        <input type="text" name="birth_date" placeholder="YYYY-MM-DD" class="ui calendar" id="id_birth_date" />
      </div>
    </div>
  </div>
  *****/
  if (!$) {$ = django.jQuery;}
  $.fn.calendarWidget = function() {
    $(this).calendar({
      monthFirst: false,
      type: 'date',
      today: 'true',
      formatter: {
        date: function (date, settings) {
          if (!date) return '';
          return date.toLocaleString(
            'en-us', {year: 'numeric', month: '2-digit', day: '2-digit'}
            ).replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2');
        }
      }
    });
  }
})(jQuery);

$(document).ready(function(){
  $('.ui.calendar').calendarWidget();
});
