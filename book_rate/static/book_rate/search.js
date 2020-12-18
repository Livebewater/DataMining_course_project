$(document).ready(function () {
    let click_flag = false;
    let click_type;
    $(".type-button").click(function () {

        click_flag = click_flag !== true;
        if (click_flag === true) {
            $(this).css({"background-color": "#5897fb"});
            click_type = $(this).attr("name")
            $(this).parent().siblings("div").children("button").attr("disabled", "disabled");
        } else {
            $(this).css({"background-color": ""});
            $(this).parent().siblings("div").children("button").removeAttr("disabled");
        }
    })
    $(".input .button").click(function () {
        let search_text = $(".input .text").val();
        if (click_flag === false) {
            alert("请先选择查找类型")
        } else if (search_text.length === 0) {
            alert("请输入")
        } else {
            let result = $(".result")
            result.children().remove()
            $.post(
                "/search/result/", {
                    "type": click_type,
                    "context": search_text
                }, function (data) {
                    data = JSON.parse(data);
                    let res = JSON.parse(data["res"]);
                    let scores = data["scores"];
                    if (res.length === 0) {
                        result.append("<li> Nothing...</li>")
                    }
                    for (let i = 0; i < res.length; i++) {
                        result.append("<li><div class='rate-box-1'><p class='isbn'>" +"isbn: "+ res[i]["pk"] + "</p><p>" + res[i]["fields"]["title"] + "</p><p>" + res[i]["fields"]["author"]
                            + "</p><p>" + res[i]["fields"]["publisher"] + "</p><p>" + res[i]["fields"]["year_of_publication"] +
                            "</p><p class='score'>"+scores[i]+"</p></div><div class='rate-box-2'><input class='add_rate' type='submit' value='添加/修改 评分'></div></li>"
                        )
                    }
                    $(".add_rate").click(function () {
                        if (data["user_id"] === undefined) {
                            alert("please login");
                            window.location.replace("/accounts/login");
                        } else {
                            let new_score = prompt("enter the new rate");
                            let box1 = $(this).parent().siblings(".rate-box-1")
                            let isbn_id = box1.children(".isbn").text().substring(6);
                            let score = box1.children(".score");
                            console.log(score);
                            $.post("/accounts/" + data["user_id"]+ "/add_rate", {"new_score": new_score,"isbn":isbn_id}, function (data) {
                                console.log("success")
                                data = JSON.parse(data);
                                if (data["status"]===1){
                                    score.text(new_score)
                                }
                            })
                        }
                    })
                }
            );

        }
    })
})
