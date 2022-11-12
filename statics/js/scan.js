window.addEventListener("load", () => {
    //dom variables (~jank?)
    window.video = document.getElementById("video");
    window.upcText = document.getElementById("upc-text");
    window.upcDetails = document.getElementById("upc-details");

    //get an api key from server
    setApiKey();

    //request camera permission
    reqCamera();

    //initialize quagga and start processing
    startQuagga();
});

function setApiKey() {
    fetch(`https://expired.deta.dev/api/key`)
    .then((res) => {
        return res.json();
    })
    .then((data) => {
        window.apiKey = data;
    })
    .catch((err) => {
        console.error(err);
    });
}

function reqCamera() {
    //actually request camera permission
    navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
            facingMode: "environment"
        }
    }).then((mediaStream) => {
        //set video element source to camera stream
        video.srcObject = mediaStream;
        //video = document.getElementsByTagName("video")[0];
        //video.play();
    }).catch((err) => {
        console.error(err);
    });
}

function startQuagga() {
    //initial quagga
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: video
        },
        frequency: 30,
        decoder: {
            readers: ["upc_reader"]
        }
    }, (err) => {
        if(err) {
            console.error(err);
            return;
        }
        console.log("ready");
        Quagga.start();
    });

    //quagga processing
    Quagga.onProcessed((data) => {
        if(!data) return;

        //update upc if it exists then other info
        if(!data.codeResult) return;

        //display upc
        upcText.innerHTML = data.codeResult.code;

        //request data via upc and respond to it
        reqByUPC(apiKey, data.codeResult.code, respond);

        //stop scanning
        Quagga.stop();
    });
}

function respond(data) {
    console.log(data);

    //check if product exists in spoonacular db
    if(data.status != undefined) {
        //~ do thing when product not found

        updateDom(false);
        return false;
    }

    //otherwise save this id, upc, title, image object
    window.productInfo = {
        id: data.id,
        upc: data.upc,
        title: data.title,
        image: data.image
    };

    //~ do stuff

    updateDom(productInfo);
    return productInfo;
}

function updateDom(productInfo) {
    if(!productInfo) {
        //product not found in db
        upcDetails.innerHTML = "nonexistent";
        return;
    }
    //change dom
    upcDetails.innerHTML = JSON.stringify(productInfo);
}

/*
function retry() {
    showAllCont();
    camPerms();
    document.getElementsByTagName("video")[0].play();
    Quagga.start();
}
*/
