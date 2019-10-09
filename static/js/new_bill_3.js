$(document).ready(function () {
    
    // Predict
    $('#btn_new_bill').click(function () {
        
        // Show loading animation
        console.log('comes here');

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/btn_new_bill',
            data: 'data_click',
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (resp) {
                // Get and display the result
                $("td").remove();
                $("#total").remove();
                console.log('comes here');
                console.log(resp);
            },
        });
    });
});
