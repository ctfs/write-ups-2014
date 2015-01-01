<?php
show_source(__FILE__);
$v1=0;$v2=0;$v3=0;$v4=0;
$a=(array)json_decode(@$_GET['a']);
if(is_array($a)){
    is_numeric(@$a["a1"])?die("nope"):NULL;
    if(@$a["a1"]){
        ($a["a1"]>1336)?$v1=1:NULL;
    }
    if(is_array(@$a["a2"])){
        if(count($a["a2"])!==5 OR !is_array($a["a2"][0])) die("nope");
        $pos = array_search("ctf", $a["a2"]);
        $pos===false?die("nope"):NULL;
        foreach($a["a2"] as $key=>$val){
            $val==="ctf"?die("nope"):NULL;
        }
        $v2=1;
    }
}
if(preg_match("/^([0-9]+\.?[0-9]+)+$/",@$_GET['b'])){
    $b=json_decode(@$_GET['b']);
    if($var = $b === NULL){
        ($var===true)?$v3=1:NULL;
    }
}
$c=@$_GET['c'];
$d=@$_GET['d'];
if(@$c[1]){
    if(!strcmp($c[1],$d) && $c[1]!==$d){
        eregi("3|1|c",$d.$c[0])?die("nope"):NULL;
        strpos(($c[0].$d), "31c3")?$v4=1:NULL;
    }
}
if($v1 && $v2 && $v3 && $v4){
    include "flag.php";
    echo $flag;
}
?>
