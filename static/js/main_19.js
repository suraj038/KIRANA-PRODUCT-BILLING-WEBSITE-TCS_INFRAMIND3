$(document).ready(function () {
    
    // Predict
    $('#btn-predict').click(function () {
        
        // Show loading animation
        console.log('comes here');
        var i = 1;
        var j = 2;

        var final_cost = 0;

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/item_data',
            data: 'data_click',
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (resp) {
                // Get and display the result
                console.log('comes here');
                console.log(resp.result);

                $("td").remove();
                $("#total").remove();

                for( i=0; i<resp.result.length; i++)
                {
                    var total_price = resp.result[i]['price'] * resp.result[i]['quantity'];
                    final_cost = Number(final_cost + total_price);
                    $("#item_data").append("<tr><td scope='row' >" + Number(i+1) + "</td><td>" + resp.result[i]['item_id'] + "</td><td>" + resp.result[i]['item_name'] +  " " + resp.result[i]['item_size'] + "</td>" + "<td>" + resp.result[i]['quantity'] + "</td><td>" + resp.result[i]['price'] + "</td><td>" + total_price + "</td></tr>");
               
                }
                $("#total_price").append("<th id='total'>Total Cost :" + Number(final_cost) + "</th>");
            },
        });
    });
});
