/**
 * Created by reonard on 16/2/25.
 */

    $(function() {
        $("#id_terminal_no").keyup(function () {
            var terminal_no_val = $("#id_terminal_no").val()
            $.ajax({
                type:"GET",
                url:"/ticketmgr/get_terminal_info/",
                data:{terminal_no:terminal_no_val},
                dataType:"json",
                success:function(result){
                    $("#id_terminal_name").text(result.terminal_name)
                    $("#id_terminal_location").text(result.terminal_location)
                }
            })
        })

        $('#id_deliver_time,#id_take_time').datetimepicker({format: 'yyyy/mm/dd hh:ii:ss'});

        $("#id_owner").typeahead({
            source:  function(query, process){
            var department_val = $("#id_department").val()
            var owner_val = $("#id_owner").val()
            $.ajax({
                type:"GET",
                url:"/ticketmgr/user_hint/",
                data:{department:department_val, owner_hint: owner_val},
                dataType:"json",
                success: function(result){
                    process(result.user_list);
                },
                error: function(){alert("eeee")}
            })
        }})
    })


    $(function() {
        $("#id_assign_to_user").typeahead({
            source: function (query, process) {
                var department_val = $("#id_assign_to_dep").val()
                var owner_val = $("#id_assign_to_user").val()
                $.ajax({
                    type: "GET",
                    url: "/ticketmgr/user_hint/",
                    data: {department: department_val, owner_hint: owner_val},
                    dataType: "json",
                    success: function (result) {
                        process(result.user_list);
                    },
                    error: function () {
                        alert("eeee")
                    }
                })
            }
        })

        $("#action_form_btn").click(function(){
            var ajax_option={url:"/ticketmgr/create_action/{{ incident_id }}/", type:"POST", success:function(data){alert(data);$(".modal-content").innerHTML=data}}
            $("#action_form").ajaxSubmit(ajax_option)

        })
    })