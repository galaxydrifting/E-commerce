console.log("working fine")

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function(resp){
            console.log("Comment saved to DB");

            if(resp.bool == true){
                $("#review-resp").html("Review added successfully.");
            }
        }
    })
})