function submitSlippi(event) {
    var slippiID = event.target.elements.slippiName.value;
    //Switch this with a full function that correctly identifies id 
    if(slippiID.indexOf('#') < 0){
        alert(slippiID + " Is not a valid Slippi ID");
        returnToPreviousPage(event);
        return false;
    }
    else{
        alert(slippiID + "Accepted!");
    }
    }

function returnToPreviousPage(event){
    event.preventDefault();
}