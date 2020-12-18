$(document).ready(function () {
    $(".button").click(function () {
        let account = $(".name");
        let password = $(".password");
        if (account.val().length === 0) {
            alert("name should not be empty")
        } else if (password.val().length === 0) {
            alert("password should not be empty")
        } else {
            $.post("login_process", {
                "name": account.val(), "password": password.val()
            }, function (data) {
                data = JSON.parse(data);
                if (data.flag === 0) {
                    alert("password error!");
                    password.val("");
                } else if (data.flag === -1) {
                    alert("user not exist!");
                    account.val("")
                    password.val("")
                } else {
                    window.location.replace(data["user_id"]);
                }
            })
        }
    })
})