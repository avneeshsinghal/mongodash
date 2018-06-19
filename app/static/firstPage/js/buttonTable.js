// SCRIPT FOR GETTING RESULT FROM DATABASE AS JSON OBJECT AND SEND TO   --> CreateTableFromJson(object)<---

$(document).ready(function () {
    $('#dyntable').DataTable({
        columnDefs: [{
            targets: [0, 1, 2],
            className: 'mdl-data-table__cell--non-numeric'
                }]
    });

});

$(document).ready(function () {

    $("#getResult").click(function () {


        $('#showData').empty();

        //var tabname = document.getElementById("selected_options").value;//use jquery instead of Javascript api

        //window.alert(id);
        tbl1 = $("#tbl1").val();
        tbl2 = $("#tbl2").val();
        key1 = $("#key1").val();
        key2 = $("#key2").val();
        value1 = $("#value1").val();
        value2 = $("#value2").val();
        action1 = $("#action1").val();
        action2 = $("#action2").val();



        var params = {

            "tbl1": tbl1,

            "tbl2": tbl2,


            "key1": key1,


            "key2": key2,


            "value1": value1,

            "value2": value2,


            "action1": action1,

            "action2": action2,
        };




        if (params["value1"] === "" || params["key1"] === "") {
            params["key1"] = "";
            params["action1"] = "";
        }
        if (params["value2"] === "" || params["key2"] === "") {
            params["key2"] = "";
            params["action2"] = "";
        }

        var flag = 0;
        var url = "http://" + $('#address1').val() + ":4000/table";




        for (var key in params) {
            if (params[key] !== "") {

                if (flag === 1) {
                    url = url.concat("&" + key + "=" + params[key]);
                }
                if (flag === 0) {
                    url = url.concat("?" + key + "=" + params[key]);
                    flag = flag + 1;
                }

            }
        }



        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (result) {


                var response = result;
                var output = [];

                //for nested table interface
                /* for(record of info){ 
                        
                        if (record.relation.length !== 0)      
                    {   record.relation=CreateTableFromJSON(record.relation).outerHTML
                        output.push(record)
                        console.log(record) 
                    } 
                        CreateTableFromJSON(output);
                        
                    }
                */

                for (record of response) {

                    mergedObj = { ...record,
                        ...record.relation
                    }
                    delete mergedObj.relation;
                    output.push(mergedObj);


                }
                if (output.length !== 0) {
                    CreateTableFromJSON(output);
                }
                if (output.length === 0) {
                    alert("There is No data for this query")
                }



            }

        });

    });
});
