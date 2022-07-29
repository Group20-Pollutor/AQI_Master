<?php
    $command = escapeshellcmd('python predictor.py');
    $output = shell_exec($command);
    echo $output;
?>

