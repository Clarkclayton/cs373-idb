document.getElementById("test-button").onclick = function () {
    var req = new XMLHttpRequest();
    var url = "http://swecune.com/api/run_tests";
    req.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                alert(req.responseText);
            }
    };
    req.open("GET", url, true);
    req.send();
};
