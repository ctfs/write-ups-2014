<?php
/*
CRYPTO.PHP // Ghost in the Shellcode
Version: 0.000001

MODIFIED BSD LICENSE (Oppa CTF Style)

Copyright (c) 2014, Ghost in the SHellcode
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Also, you're a fool if you want to reuse this code. It's built for CTFs, that alone should scare you off...

error_reporting(-1);
*/


$valid_functions = array('help', 'dump', 'test','customCrypto');

/*
    from http://borkweb.com/story/a-simple-server-side-ajax-handler
    Not originally secure, but sanitizing the data makes it safe!
*/

if(isset($_POST['function']) && in_array($_POST['function'],$valid_functions))
{
    $params = $_POST;
    unset($params['function']);

    $param_string='';
    foreach($params as $key=>$param)
    {
        $param = preg_replace('/[^A-Za-z0-9]/','',$param);
        $param_string.=(($param_string)?',':'')."'".$param."'";
    }

    if (isset($DEBUG) && $DEBUG == "true") { error_log($_POST['function']."($param_string);"); }
    eval("echo ".$_POST['function']."($param_string);");
} else {
    if (isset($_POST['function']))
    {
        echo json_encode(array("error"=>"true", "errorMsg"=>"invalid function name"));
    }
 }

function docs()
{
    return json_encode("GITS Custom Crypto 2.4b. Written with PHP so it's sure to be secure.");
}

function dump()
{
    return highlight_file(__FILE__,true);
}

function test()
{
    $arr = array('a' => 1, 'b' => 2, 'c' => 3, 'd' => 4, 'e' => 5);
    return json_encode($arr);
}

function customCrypto($key,$plaintextHex,$DEBUG=false)
{
    $data = array();

    $xorKey = "";

    //plaintext is untrusted.
    $plaintext = pack("H*" , $plaintextHex);

    //filter unsafe characters
    $safeKey = preg_replace('/[\"\']/','',$key);

    foreach (str_split($safeKey) as $key => $value)
    {
        if (in_array($value,range('@','Z')))
        {
            $xorKey .= chr(ord($value)-29); // map upper alpha to safe ascii symbols
        } else {
            if (in_array($value,range('`','z')))
            {
                $xorKey .= chr(ord($value)-62); // map lower alpha to safe ascii symbols
            } else {
                $xorKey .= $value;
            }
        }
        // xorKey now contains non-alpha characters more suitable for secure xor (prevent dictionary attacks)
    }

    if (isset($DEBUG) && $DEBUG == "true")
    {
        //$message = "\$message = \"The key is: $xorKey and the plaintext is: \".addslashes(\"$plaintext\");";
        assert("\$message = \"The key is: $xorKey and the plaintext is: \".addslashes(\"$plaintext\");");
        error_log($message);
        $data['errorMsg'] .= $message;
    }

    // pad out xorKey in manner that frustrates cryptanalysis
    $starter = strlen($xorKey);
    $length = $starter;
    while(strlen($xorKey) < strlen($plaintext))
    {
        if ($length-- == 0) { $length = $starter; }
        $xorKey .= substr($xorKey,0,$length);
    }


    if (strlen($xorKey) < strlen($plaintext))
    {
        if (isset($DEBUG) && $DEBUG == "true")
        {
        assert("\$message = \"ERROR! xorKey is: \".strlen(\$xorKey).\" bytes long and the plaintext is: \".strlen($plaintext).\" bytes long.\";");
        $data['error'] = "true";
        $data['errorMsg'] .= $message;
        }
        return json_encode($data);
    } else {
        // abuse a "feature" of php that returns the shorter of the two strings xor'ed with the relevant bits of the longer
        $data['returnValue'] = bin2hex(substr(($plaintext^$xorKey),0, strlen($plaintext)));
        if (isset($DEBUG) && $DEBUG == "true") { error_log(json_encode($data)); };
        return json_encode($data);

    }
}
?>