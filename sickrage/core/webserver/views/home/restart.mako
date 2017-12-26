<%!
    import sickrage
%>

<meta data-var="srWebRoot" data-content="${srWebRoot}">
<meta data-var="srDefaultPage" data-content="${srDefaultPage}">
<%block name="metas" />

<link rel="stylesheet" type="text/css" href="${srWebRoot}/css/bower.min.css"/>
<%block name="css" />

<%block name="content">
    <div class="text-center">
        <h2>${_('Performing Restart')}</h2>
        <div class="progress center-block" style="width:50%">
            <div id="dynamic" class="progress-bar progress-bar-striped active" role="progressbar" style="width: 25%">
                25% Complete
            </div>
        </div>
        <div id="message">Waiting for SiCKRAGE to shut down</div>
    </div>
</%block>

<script src="${srWebRoot}/js/bower.min.js"></script>
<script>
    var current_pid = '';
    var timeout_id;
    var num_restart_waits = 0;
    var srWebRoot = $('meta[data-var="srWebRoot"]').data('content');
    var srDefaultPage = $('meta[data-var="srDefaultPage"]').data('content');

    (function checkIsAlive() {
        timeout_id = 0;

        $.ajax({
            url: srWebRoot + '/home/is_alive/',
            dataType: 'jsonp',
            jsonp: 'srcallback',
            success: function (data) {
                if (data.msg === 'nope') {
                    $("#dynamic").css("width", "50%").text("50% Complete");
                    setTimeout(checkIsAlive, 1000);
                } else {
                    if (current_pid === '' || data.msg === current_pid) {
                        current_pid = data.msg;
                        setTimeout(checkIsAlive, 1000);
                    } else {
                        $("#dynamic").css({"width": "100%", 'background-color': 'green'}).text("100% Complete");
                        $("#message").text("Loading the home page");
                        window.location = srWebRoot + '/' + srDefaultPage + '/';
                    }
                }
            },
            error: function (error) {
                num_restart_waits += 1;

                $("#dynamic").css("width", "75%").text("75% Complete");
                $("#message").text("Waiting for SiCKRAGE to start again");

                // if it is taking forever just give up
                if (num_restart_waits > 90) {
                    $("#dynamic").css({"width": "100%", 'background-color': 'red'}).text("100% Failed");
                    $("#message").text("The restart has timed out, perhaps something prevented SiCKRAGE from starting again?");
                    return;
                }

                if (timeout_id === 0) {
                    timeout_id = setTimeout(checkIsAlive, 1000);
                }
            }
        });
    })();
</script>
<%block name="scripts" />