<!DOCTYPE html>
<?php
$myfile = fopen("SlippiNameData.txt", "w") or die("Unable to open file!");
$txt = $_GET["slippiName"];
fwrite($myfile, $txt);
fclose($myfile);
$fullname = "python C:\Users\\ethan\Desktop\csciAIProject\\example.py --port 1 --opponent 2 --connect_code DJAR#173 --dolphin_executable_path \"C:\Users\\ethan\AppData\Roaming\Slippi Launcher\\netplay\"";
system($fullname);
//exec("python C:\\Users\\ethan\\Desktop\\csciAIProject\\example.py --port 1 --opponent 2 --connect_code DJAR#173 --dolphin_executable_path \'C:\\Users\\ethan\AppData\\Roaming\\Slippi Launcher\\netplay\'");



?>
<html> 
    <head>
        <link rel="stylesheet" type="text/css" href="CSS/style.css">
        <meta charset="UTF-8">
        <meta name="descrpition" content="A website to connect to a melee AI that helps train your tech chasing skill">
        <meta name="authoer" contents="Ethan Kane">
        <meta name="viewport" conent="width=device-width, initial-scale=1.0">
        <title>Melee Trainer</title>
    </head>

    <body> 
       <header>
            
            <img class = foxImage src="pngfind.com-shine-png-582761.png" alt="Fox Image">
           
            <h1> Melee Trainer</h1>

            <p class= "ogDescription"> 
                This website is a simple and in develpoment tool to help learn how to tech in melee with simple AI assistance
                <br>
                More information can be found in my <a href="https://github.com" target="_blank"> Replace this with my github page</a> 
                or my <a href="https://github.com" target="_blank"> Replace this with my Website page</a>
            </p>

       </header>
       
       <main>
        <hr>
        Your name "<?php echo("$txt"); ?>" is submitted, now connect on slippi to the AI!
        <p>

            
        </p>






       </main>
       <footer>


       </footer>


       
       
        <!-- <h1>Melee Trainer</h1>
        <p>You will need a couple simple things before facing this wonderful ai</p>
        <p style="color: red; background-color:blue;"> Testing to see if this works</p> </p> -->
    </body>

</html>