$(document).ready(function () {
    $(".button").click(function () {
        let account = $(".name");
        let password = $(".password");
        let location = $(".location");
        let age = $(".age");
        if (account.val().length === 0) {
            alert("name should not be empty")
        } else if (location.val().length === 0) {
            alert("location should not be empty")
        } else if (age.val().length === 0) {
            alert("age should not be empty")
        } else if (password.val().length === 0) {
            alert("password should not be empty")
        } else {
            $.post(
                "signup_process", {
                    "name": account.val(), "location": location.val(), "password": password.val(), "age": age.val()
                }, function (data) {
                    data = JSON.parse(data);
                    if (data["flag"] === 0) {
                        alert("user have be signup!");
                        window.location.replace(data["user_id"]);
                    }
                    else if(data["flag"]===-1){
                        alert("user have be exist!")
                        account.val("")
                        password.val("")
                        location.val("")
                        age.val("")
                    }
                    else {
                        window.location.replace(data["user_id"]);
                    }

                }
            )
        }
    })
})