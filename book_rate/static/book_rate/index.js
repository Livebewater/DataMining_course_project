$(document).ready(function () {
    let load = $(".loading").hide();
    load.click(function f() {
        $(".loading").toggle(["slow", "swing", "loading-none"])
    })
})