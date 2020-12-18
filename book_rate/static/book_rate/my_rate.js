$(document).ready(function () {
    $(".delete").click(function () {
        let confirm_flag = confirm("yes?");
        if (confirm_flag === true){
            let rate = $(this);
            let isbn_id = rate.siblings(".isbn").text().substring(6);
            $.post(
                "delete", {"isbn": isbn_id}, function (data) {
                    data = JSON.parse(data);
                    if (data.flag === 1){
                        rate.parent().remove();
                    }
                    else{
                        alert("delete error");
                    }
                }
            )
        }
    })
    $(".alter").click(function () {
        let rate = $(this);
        let new_score = prompt("enter the new rate");
        let isbn_id = rate.siblings(".isbn").text().substring(6);
        $.post("my_rate/alter", {"isbn": isbn_id, "new_score": new_score}, function (data) {
                    data = JSON.parse(data);
                    if (data.flag === 1){
                         rate.siblings(".score").text("score: "+new_score);
                    }
                    else{
                        alert("alter error");
                    }
        })
    })
})