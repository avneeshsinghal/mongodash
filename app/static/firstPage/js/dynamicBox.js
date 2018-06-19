//SCRIPT FOR DYNAMICALLY CREATING DROPDOWN TABLE LIST


function CreateDatalist() {


    var all_table_list = ["user_det", "route_det", "bus", "trip"];

    var create_option = '<datalist id ="tbl1"   >';


    for (i = 0; i < all_table_list.length; i++) {

        create_option = create_option + '<option value="' + all_table_list[i] + '" id = "' + all_table_list[i] + '">' + all_table_list[i] + '</option>';

    }
    create_option = create_option + '</datalist>';

    $("#createlist").append(create_option);
};

$(document).ready(function () {


    changeHandler(); // setting event handlers on edit.



    $.ajax({
        url: "http://localhost:4000/get_all_tables",
        type: 'GET',
        dataType: 'json',
        success: function (result) {



            var all_table_list = result;

            var create_option = '';


            for (i = 0; i < all_table_list.length; i++) {

                create_option = create_option + '<option value="' + all_table_list[i] + '" id = "' + all_table_list[i] + '">' + all_table_list[i] + '</option>';

            }


            $("#create_table_list1").append(create_option);
            $("#create_table_list2").append(create_option);
        }
    });
});





function changeHandler() {

    $("#tbl1").change(function () {

        table1 = "tbl1=" + $("#tbl1").val();

        if($("#tbl1").val()==="")
        {
            $("#create_key_list1").empty();

            $("#key1").prop('disabled',true);

            $("#key1").prop('value',"");
        }
        else
        { $("#key1").prop('disabled',false);}







        $.ajax({
            url: "http://localhost:4000/get_tbl1_keys?" + table1,
            type: 'GET',
            dataType: 'json',
            success: function (result) {

                var all_table_list = result;

                var create_option = '';


                for (i = 0; i < all_table_list.length; i++) {

                    create_option = create_option + '<option value="' + all_table_list[i] + '" id = "' + all_table_list[i] + '">' + all_table_list[i] + '</option>';

                }


                $("#create_key_list1").empty();
                $("#create_key_list1").append(create_option);

            }
        });
    });

    $('#tbl2').change(function () {


         if($("#tbl2").val()==="")
        {
            $("#create_key_list2").empty();
            $("#key2").prop('disabled',true);
          $("#key2").prop('value',"");
        }
        else
        { $("#key2").prop('disabled',false);}


        table2 = "tbl2=" + $("#tbl2").val();
        $.ajax({
            url: "http://localhost:4000/get_tbl2_keys?" + table2,
            type: 'GET',
            dataType: 'json',
            success: function (result) {



                var all_table_list = result;

                var create_option = '';

                for (i = 0; i < all_table_list.length; i++) {
                    create_option = create_option + '<option value="' + all_table_list[i] + '" id = "' + all_table_list[i] + '">' + all_table_list[i] + '</option>';
                }



                $("#create_key_list2").empty();
                $("#create_key_list2").append(create_option);

            }
        });


    });

  /*   $('#key2').change(function () {
         if ($("#key2").val() === "") {
             $("#action2").prop('disabled', true);
             $("#value2").prop('disabled', true);
             //$("#action2").prop('value', "");
             //$("#value2").prop('value', "");
         }
         else {
             $("#action2").prop('disabled', false);
             $("#value2").prop('disabled', false);
         }

     });*/

}





/*
//SCRIPT FOR DYNAMICALLY CREATING TEXT-FIELD
        var param = 1;
        $(document).ready(function() {
            $(document.getElementById("addMore")).on("click", function() {

                var row = '<br><input type="text" name=param' + param + ' placeholder="enter a key "/>';
                param = param + 1;

                $("#keys").append(row);
            });
        });
*/
