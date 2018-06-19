function CreateTableFromJSON(data) {

    // EXTRACT VALUE FOR HTML HEADER.
    var col = [];
    for (var i = 0; i < data.length; i++) {
        for (var key in data[i]) {
            if (col.indexOf(key) === -1) {
                col.push(key);
            }
        }
    }

    // CREATE DYNAMIC TABLE.
    var table = document.createElement("table");
    var header = table.createTHead();
    var body = table.createTBody();

    // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

    var headerRow = header.insertRow();

    for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th"); // TABLE HEADER.
        th.innerHTML = col[i];
        headerRow.appendChild(th);
    }


    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < data.length; i++) {

        tr = body.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
            var tabCell = tr.insertCell(-1);
            tabCell.innerHTML = data[i][col[j]];
        }
    }

    // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
    table.setAttribute("id", "dyntable");
    table.setAttribute("class", "display")
    var divContainer = document.getElementById("showData");

    divContainer.innerHTML = "";
    divContainer.appendChild(table);
    $('#dyntable').DataTable();
    return table
}
