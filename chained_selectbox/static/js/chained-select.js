(function($) {
    $(document).ready(function() {

        $.fn.loadChainedChoices_getInLoop = function(ajax_url, valuefield, parent_value) {
            $.get(ajax_url, {field: valuefield.attr('name').split('-')[2], parent_value: parent_value}, function(j) {
                var options = '';
                for (var i = 0; i < j.length; i++) {
                    options += '<option value="' + j[i][0] + '">' + j[i][1] + '</option>';
                }

                valuefield.html(options);
                valuefield.trigger('change');
            }, "json");
        };

        $.fn.loadChainedChoices = function() {
            for (var idx = 0 ; idx < 512 ; idx++) {
                if ($(this).attr('chained_id'+idx) == undefined) {
                    break;
                }
                var chained_id = $(this).attr('chained_id'+idx);
                if (chained_id.indexOf('__prefix__') != -1) {
                    chained_id = chained_id.replace('__prefix__', $(this).attr('name').split('-')[1]);
                    $(this).attr('chained_id'+idx, chained_id);
                }

                var valuefield = $('#' + chained_id);
                var ajax_url = valuefield.attr('ajax_url');

                $(this).loadChainedChoices_getInLoop(ajax_url, valuefield, $(this).val());
            }
        };
        /* This part of code is replaced in widgets.py
           $('.chained-parent-field').on('change', function(e) {
               console.log("sono li");
               $(this).loadChainedChoices();
           });
        */
    });
})(django.jQuery);




