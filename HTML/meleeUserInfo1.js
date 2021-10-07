
function submitSlippi(event) {
    event.preventDefault();
    var slippiID = event.target.elements.slippiName.value;
    //Switch this with a full function that correctly identifies id 
    if(detectProperSlippiID(slippiID)){
        console.log(slippiID + "Accepted! test");
        var xhr = new XMLHttpRequest();
        xhr.open('Post', 'slippiAction.php', true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        var postParam = "slippiName="+slippiID.toUpperCase();
        //console.log(slippiID+ "Did we Get here? Name is "+ 'slippinameaction.php?slippiName='+slippiID);
        xhr.onload = function(){
            console.log(this.responseText);
            console.log("Got here1");
            document.getElementById("phpform").innerHTML = this.responseText;
        }
        xhr.send(postParam);
        console.log("Got to end of function");
        return true;
    }
    else{
        alert(slippiID + " Is not a valid Slippi ID");
        //returnToPreviousPage(event);
        return false;
    }
}






function returnToPreviousPage(event){
    event.preventDefault();
}

function detectProperSlippiID(slippiString){
    // In case name length changes later
    var maxNameLength = 8;
    if(slippiString.length > maxNameLength){
        return false;
    }
    // I dont think names can start with a hashtag? Also assuming hashtag cant be the final letter, will fix if I learn this isnt true
    var tagIndex = slippiString.indexOf('#')
    if(tagIndex < 1 || tagIndex > maxNameLength-2){
        return false;
    }
    else{
        for(var i = tagIndex+1; i < slippiString.length; i++){
            if(slippiString.charAt(i) < '0' || slippiString.charAt(i) > '9'){
                return false;
            }
        }
    }
    return true;
}


function loadDoc(){
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      document.getElementById("demo").innerHTML = this.responseText;
    }
    xhttp.open("GET", "SlippiNameData.txt");
    xhttp.send();

}

function testFunction(){
    alert("This is a test");
}