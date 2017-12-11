// COURSE: CST 205 - Multimedia Design & Programming
// TITLE: grid.js
// ABSTRACT: Used to receive json data and populate ag-grid.
// AUTHORS: Erick Shaffer
// DATE: 12/10/17
document.addEventListener("DOMContentLoaded", function () {
    var columnDefs = [
        {headerName: "Name", field: "name"},
        {
            headerName: "Link",
            field: "full_link",
            cellRenderer: function(params) {
                return "<a href= '" + encodeURIComponent(params.value) + "' target='_blank'>"+ params.value+ "</a>"
}
        },
        {headerName: "views", field: "views"},
        {headerName: "Date Added", field: "time_created"}
    ];

    var gridOptions = {
        columnDefs: columnDefs,
        enableFilter: true,
        enableSorting: true,
        animateRows: true,
        sortingOrder: ['desc', 'asc', null],
        onGridReady: function () {
            gridOptions.api.sizeColumnsToFit();
            gridOptions.api.showLoadingOverlay()
        }
    };

    var eGridDiv = document.querySelector('#myGrid');
    new agGrid.Grid(eGridDiv, gridOptions);

    jsonLoad(function(data) {
        console.log(data)
        gridOptions.api.setRowData(data);
    })
});

function selectAllRows() {
    gridOptions.api.selectAll()
}


function jsonLoad(callback) {
        $.ajax({
            type: "POST",
            url: "/api/links",
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                // console.log(data);
                callback(JSON.parse(data));
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
}



