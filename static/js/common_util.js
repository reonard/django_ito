/**
 * Created by reonard on 16/3/31.
 */

function autofil_maitainer(terminal_no, fill_field){
        $.get("/ticketmgr/get_maintainer/",{terminal_no:terminal_no},
        function(result){
            fill_field.val(result.maintainer)
        })
}