//modal delete
$(document).ready(function () {

    $('.btn-click-del').on('click', function () {
        $("#mi-modal").modal('show');
        title = $(event.currentTarget).closest('tr').children('td').first().text();
        componentName = $(this).data('name');
        $("#myModalLabel").html("Would you like to delete " + componentName +": " + title + "?");
        $("#modal-btn-yes").data('id', $(this).data('id'));
    });

    $('body').on('click', '#modal-btn-yes', function () {
        var id = $(this).data('id');
        $("#mi-modal").modal('hide');
        location.href = urlDelete(id);
    });

    $("#modal-btn-no").on("click", function(){
        $("#mi-modal").modal('hide');
    });

    function urlDelete(id){
        return window.location.protocol + '//' +  window.location.host + '/' + location.pathname.split('/')[1] + '/' + id + '/' + "remove";
    }

});
