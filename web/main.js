eel.expose(set_directory);
function set_directory(data) {
    document.getElementById("input-directory").value = data["input_directory"];
    document.getElementById("output-directory").value = data["output_directory"];
    document.getElementById("amplitude").value = data["amplitude"];
};

async function run(){
    const data = {
        "input": document.getElementById("input-directory").value,
        "output": document.getElementById("output-directory").value,
        "mode": document.getElementById("mode-selection").value,
        "num": parseInt(document.getElementById("amplitude").value),
    };
    const res = await eel.run(data)();

    alert(res)
};

eel.expose(set_progressbar);
function set_progressbar(msg, progress_rate) {
    console.log(progress_rate);
    document.getElementById("progressbar-msg").innerText = msg;
    document.getElementById("progressbar").style.width = `${progress_rate}%`;
};