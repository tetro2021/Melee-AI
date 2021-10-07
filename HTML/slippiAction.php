<?php
//$myfile = fopen("SlippiNameData.txt", "w") or die("Unable to open file!");
$txt = $_POST["slippiName"];
//echo($txt);
//fwrite($myfile, $txt);
//fclose($myfile);
$fullname = escapeshellcmd("python C:\Users\\ethan\Desktop\csciAIProject\\example.py --port 1 --opponent 2 --connect_code " . $txt . " --dolphin_executable_path \"C:\Users\\ethan\AppData\Roaming\Slippi Launcher\\netplay\"");
//echo '<button type="button" onclick="testFunction()">' . $fullname . '</button>';
//$python = system($fullname);
//echo $python;
system($fullname);
//exec("python C:\\Users\\ethan\\Desktop\\csciAIProject\\example.py --port 1 --opponent 2 --connect_code DJAR#173 --dolphin_executable_path \'C:\\Users\\ethan\AppData\\Roaming\\Slippi Launcher\\netplay\'");
?>