	.686P
	.model	flat

PUBLIC  text_text
PUBLIC	l_key
PUBLIC	s_box
PUBLIC	add_1
PUBLIC	f
PUBLIC	f_rnd
PUBLIC	i_rnd
PUBLIC	k_rnd
PUBLIC	set_key
PUBLIC	encrypt
PUBLIC	decrypt
PUBLIC	main

_BSS SEGMENT
l_key DD 060H DUP (?)
_BSS ENDS

_TEXT SEGMENT
text_text DB "Secret out crypto ...", 0 ; test phrase to encrypt/decrypt in standalone version
s_box DD 030fb40d4H
	DD	09fa0ff0bH
	DD	06beccd2fH
	DD	03f258c7aH
	DD	01e213f2fH
	DD	09c004dd3H
	DD	06003e540H
	DD	0cf9fc949H
	DD	0bfd4af27H
	DD	088bbbdb5H
	DD	0e2034090H
	DD	098d09675H
	DD	06e63a0e0H
	DD	015c361d2H
	DD	0c2e7661dH
	DD	022d4ff8eH
	DD	028683b6fH
	DD	0c07fd059H
	DD	0ff2379c8H
	DD	0775f50e2H
	DD	043c340d3H
	DD	0df2f8656H
	DD	0887ca41aH
	DD	0a2d2bd2dH
	DD	0a1c9e0d6H
	DD	0346c4819H
	DD	061b76d87H
	DD	022540f2fH
	DD	02abe32e1H
	DD	0aa54166bH
	DD	022568e3aH
	DD	0a2d341d0H
	DD	066db40c8H
	DD	0a784392fH
	DD	04dff2fH
	DD	02db9d2deH
	DD	097943facH
	DD	04a97c1d8H
	DD	0527644b7H
	DD	0b5f437a7H
	DD	0b82cbaefH
	DD	0d751d159H
	DD	06ff7f0edH
	DD	05a097a1fH
	DD	0827b68d0H
	DD	090ecf52eH
	DD	022b0c054H
	DD	0bc8e5935H
	DD	04b6d2f7fH
	DD	050bb64a2H
	DD	0d2664910H
	DD	0bee5812dH
	DD	0b7332290H
	DD	0e93b159fH
	DD	0b48ee411H
	DD	04bff345dH
	DD	0fd45c240H
	DD	0ad31973fH
	DD	0c4f6d02eH
	DD	055fc8165H
	DD	0d5b1caadH
	DD	0a1ac2daeH
	DD	0a2d4b76dH
	DD	0c19b0c50H
	DD	0882240f2H
	DD	0c6e4f38H
	DD	0a4e4bfd7H
	DD	04f5ba272H
	DD	0564c1d2fH
	DD	0c59c5319H
	DD	0b949e354H
	DD	0b04669feH
	DD	0b1b6ab8aH
	DD	0c71358ddH
	DD	06385c545H
	DD	0110f935dH
	DD	057538ad5H
	DD	06a390493H
	DD	0e63d37e0H
	DD	02a54f6b3H
	DD	03a787d5fH
	DD	06276a0b5H
	DD	019a6fcdfH
	DD	07a42206aH
	DD	029f9d4d5H
	DD	0f61b1891H
	DD	0bb72275eH
	DD	0aa508167H
	DD	038901091H
	DD	0c6b505ebH
	DD	084c7cb8cH
	DD	02ad75a0fH
	DD	0874a1427H
	DD	0a2d1936bH
	DD	02ad286afH
	DD	0aa56d291H
	DD	0d7894360H
	DD	0425c750dH
	DD	093b39e26H
	DD	0187184c9H
	DD	06c00b32dH
	DD	073e2bb14H
	DD	0a0bebc3cH
	DD	054623779H
	DD	064459eabH
	DD	03f328b82H
	DD	07718cf82H
	DD	059a2cea6H
	DD	04ee002eH
	DD	089fe78e6H
	DD	03fab0950H
	DD	0325ff6c2H
	DD	081383f05H
	DD	06963c5c8H
	DD	076cb5ad6H
	DD	0d49974c9H
	DD	0ca180dcfH
	DD	0380782d5H
	DD	0c7fa5cf6H
	DD	08ac31511H
	DD	035e79e13H
	DD	047da91d0H
	DD	0f40f9086H
	DD	0a7e2419eH
	DD	031366241H
	DD	051ef495H
	DD	0aa573b04H
	DD	04a805d8dH
	DD	0548300d0H
	DD	0322a3cH
	DD	0bf64cddfH
	DD	0ba57a68eH
	DD	075c6372bH
	DD	050afd341H
	DD	0a7c13275H
	DD	0915a0bf5H
	DD	06b54bfabH
	DD	02b0b1426H
	DD	0ab4cc9d7H
	DD	0449ccd82H
	DD	0f7fbf265H
	DD	0ab85c5f3H
	DD	01b55db94H
	DD	0aad4e324H
	DD	0cfa4bd3fH
	DD	02deaa3e2H
	DD	09e204d02H
	DD	0c8bd25acH
	DD	0eadf55b3H
	DD	0d5bd9e98H
	DD	0e31231b2H
	DD	02ad5ad6cH
	DD	0954329deH
	DD	0adbe4528H
	DD	0d8710f69H
	DD	0aa51c90fH
	DD	0aa786bf6H
	DD	022513f1eH
	DD	0aa51a79bH
	DD	02ad344ccH
	DD	07b5a41f0H
	DD	0d37cfbadH
	DD	01b069505H
	DD	041ece491H
	DD	0b4c332e6H
	DD	032268d4H
	DD	0c9600accH
	DD	0ce387e6dH
	DD	0bf6bb16cH
	DD	06a70fb78H
	DD	0d03d9c9H
	DD	0d4df39deH
	DD	0e01063daH
	DD	04736f464H
	DD	05ad328d8H
	DD	0b347cc96H
	DD	075bb0fc3H
	DD	098511bfbH
	DD	04ffbcc35H
	DD	0b58bcf6aH
	DD	0e11f0abcH
	DD	0bfc5fe4aH
	DD	0a70aec10H
	DD	0ac39570aH
	DD	03f04442fH
	DD	06188b153H
	DD	0e0397a2eH
	DD	05727cb79H
	DD	09ceb418fH
	DD	01cacd68dH
	DD	02ad37c96H
	DD	0175cb9dH
	DD	0c69dff09H
	DD	0c75b65f0H
	DD	0d9db40d8H
	DD	0ec0e7779H
	DD	04744ead4H
	DD	0b11c3274H
	DD	0dd24cb9eH
	DD	07e1c54bdH
	DD	0f01144f9H
	DD	0d2240eb1H
	DD	09675b3fdH
	DD	0a3ac3755H
	DD	0d47c27afH
	DD	051c85f4dH
	DD	056907596H
	DD	0a5bb15e6H
	DD	0580304f0H
	DD	0ca042cf1H
	DD	011a37eaH
	DD	08dbfaadbH
	DD	035ba3e4aH
	DD	03526ffa0H
	DD	0c37b4d09H
	DD	0bc306ed9H
	DD	098a52666H
	DD	05648f725H
	DD	0ff5e569dH
	DD	0ced63d0H
	DD	07c63b2cfH
	DD	0700b45e1H
	DD	0d5ea50f1H
	DD	085a92872H
	DD	0af1fbda7H
	DD	0d4234870H
	DD	0a7870bf3H
	DD	02d3b4d79H
	DD	042e04198H
	DD	0cd0ede7H
	DD	026470db8H
	DD	0f881814cH
	DD	0474d6ad7H
	DD	07c0c5e5cH
	DD	0d1231959H
	DD	0381b7298H
	DD	0f5d2f4dbH
	DD	0ab838653H
	DD	06e2f1e23H
	DD	083719c9eH
	DD	0bd91e046H
	DD	09a56456eH
	DD	0dc39200cH
	DD	020c8c571H
	DD	0962bda1cH
	DD	0e1e696ffH
	DD	0b141ab08H
	DD	07cca89b9H
	DD	01a69e783H
	DD	02cc4843H
	DD	0a2f7c579H
	DD	0429ef47dH
	DD	0427b169cH
	DD	05ac9f049H
	DD	0dd8f0f00H
	DD	05c8165bfH
	DD	01f201094H
	DD	0ef0ba75bH
	DD	069e3cf7eH
	DD	0393f4380H
	DD	0fe61cf7aH
	DD	0eec5207aH
	DD	055889c94H
	DD	072fc0651H
	DD	0ada7ef79H
	DD	04e1d7235H
	DD	0d55a63ceH
	DD	0de0436baH
	DD	099c430efH
	DD	05f0c0794H
	DD	018dcdb7dH
	DD	0a1d6eff3H
	DD	0a0b52f7bH
	DD	059e83605H
	DD	0ee15b094H
	DD	0e9ffd909H
	DD	0dc440086H
	DD	0ef944459H
	DD	0ba83ccb3H
	DD	0e0c3cdfbH
	DD	0d1da4181H
	DD	03b092ab1H
	DD	0f997f1c1H
	DD	0a5e6cf7bH
	DD	01420ddbH
	DD	0e4e7ef5bH
	DD	025a1ff41H
	DD	0e180f806H
	DD	01fc41080H
	DD	0179bee7aH
	DD	0d37ac6a9H
	DD	0fe5830a4H
	DD	098de8b7fH
	DD	077e83f4eH
	DD	079929269H
	DD	024fa9f7bH
	DD	0e113c85bH
	DD	0acc40083H
	DD	0d7503525H
	DD	0f7ea615fH
	DD	062143154H
	DD	0d554b63H
	DD	05d681121H
	DD	0c866c359H
	DD	03d63cf73H
	DD	0cee234c0H
	DD	0d4d87e87H
	DD	05c672b21H
	DD	071f6181H
	DD	039f7627fH
	DD	0361e3084H
	DD	0e4eb573bH
	DD	0602f64a4H
	DD	0d63acd9cH
	DD	01bbc4635H
	DD	09e81032dH
	DD	02701f50cH
	DD	099847ab4H
	DD	0a0e3df79H
	DD	0ba6cf38cH
	DD	010843094H
	DD	02537a95eH
	DD	0f46f6ffeH
	DD	0a1ff3b1fH
	DD	0208cfb6aH
	DD	08f458c74H
	DD	0d9e0a227H
	DD	04ec73a34H
	DD	0fc884f69H
	DD	03e4de8dfH
	DD	0ef0e0088H
	DD	03559648dH
	DD	08a45388cH
	DD	01d804366H
	DD	0721d9bfdH
	DD	0a58684bbH
	DD	0e8256333H
	DD	0844e8212H
	DD	0128d8098H
	DD	0fed33fb4H
	DD	0ce280ae1H
	DD	027e19ba5H
	DD	0d5a6c252H
	DD	0e49754bdH
	DD	0c5d655ddH
	DD	0eb667064H
	DD	077840b4dH
	DD	0a1b6a801H
	DD	084db26a9H
	DD	0e0b56714H
	DD	021f043b7H
	DD	0e5d05860H
	DD	054f03084H
	DD	066ff472H
	DD	0a31aa153H
	DD	0dadc4755H
	DD	0b5625dbfH
	DD	068561be6H
	DD	083ca6b94H
	DD	02d6ed23bH
	DD	0eccf01dbH
	DD	0a6d3d0baH
	DD	0b6803d5cH
	DD	0af77a709H
	DD	033b4a34cH
	DD	0397bc8d6H
	DD	05ee22b95H
	DD	05f0e5304H
	DD	081ed6f61H
	DD	020e74364H
	DD	0b45e1378H
	DD	0de18639bH
	DD	0881ca122H
	DD	0b96726d1H
	DD	08049a7e8H
	DD	022b7da7bH
	DD	05e552d25H
	DD	05272d237H
	DD	079d2951cH
	DD	0c60d894cH
	DD	0488cb402H
	DD	01ba4fe5bH
	DD	0a4b09f6bH
	DD	01ca815cfH
	DD	0a20c3005H
	DD	08871df63H
	DD	0b9de2fcbH
	DD	0cc6c9e9H
	DD	0beeff53H
	DD	0e3214517H
	DD	0b4542835H
	DD	09f63293cH
	DD	0ee41e729H
	DD	06e1d2d7cH
	DD	050045286H
	DD	01e6685f3H
	DD	0f33401c6H
	DD	030a22c95H
	DD	031a70850H
	DD	060930f13H
	DD	073f98417H
	DD	0a1269859H
	DD	0ec645c44H
	DD	052c877a9H
	DD	0cdff33a6H
	DD	0a02b1741H
	DD	07cbad9a2H
	DD	02180036fH
	DD	050d99c08H
	DD	0cb3f4861H
	DD	0c26bd765H
	DD	064a3f6abH
	DD	080342676H
	DD	025a75e7bH
	DD	0e4e6d1fcH
	DD	020c710e6H
	DD	0cdf0b680H
	DD	017844d3bH
	DD	031eef84dH
	DD	07e0824e4H
	DD	02ccb49ebH
	DD	0846a3baeH
	DD	08ff77888H
	DD	0ee5d60f6H
	DD	07af75673H
	DD	02fdd5cdbH
	DD	0a11631c1H
	DD	030f66f43H
	DD	0b3faec54H
	DD	0157fd7faH
	DD	0ef8579ccH
	DD	0d152de58H
	DD	0db2ffd5eH
	DD	08f32ce19H
	DD	0306af97aH
	DD	02f03ef8H
	DD	099319ad5H
	DD	0c242fa0fH
	DD	0a7e3ebb0H
	DD	0c68e4906H
	DD	0b8da230cH
	DD	080823028H
	DD	0dcdef3c8H
	DD	0d35fb171H
	DD	088a1bc8H
	DD	0bec0c560H
	DD	061a3c9e8H
	DD	0bca8f54dH
	DD	0c72feffaH
	DD	022822e99H
	DD	082c570b4H
	DD	0d8d94e89H
	DD	08b1c34bcH
	DD	0301e16e6H
	DD	0273be979H
	DD	0b0ffeaa6H
	DD	061d9b8c6H
	DD	0b24869H
	DD	0b7ffce3fH
	DD	08dc283bH
	DD	043daf65aH
	DD	0f7e19798H
	DD	07619b72fH
	DD	08f1c9ba4H
	DD	0dc8637a0H
	DD	016a7d3b1H
	DD	09fc393b7H
	DD	0a7136eebH
	DD	0c6bcc63eH
	DD	01a513742H
	DD	0ef6828bcH
	DD	0520365d6H
	DD	02d6a77abH
	DD	03527ed4bH
	DD	0821fd216H
	DD	095c6e2eH
	DD	0db92f2fbH
	DD	05eea29cbH
	DD	0145892f5H
	DD	091584f7fH
	DD	05483697bH
	DD	02667a8ccH
	DD	085196048H
	DD	08c4baceaH
	DD	0833860d4H
	DD	0d23e0f9H
	DD	06c387e8aH
	DD	0ae6d249H
	DD	0b284600cH
	DD	0d835731dH
	DD	0dcb1c647H
	DD	0ac4c56eaH
	DD	03ebd81b3H
	DD	0230eabb0H
	DD	06438bc87H
	DD	0f0b5b1faH
	DD	08f5ea2b3H
	DD	0fc184642H
	DD	0a036b7aH
	DD	04fb089bdH
	DD	0649da589H
	DD	0a345415eH
	DD	05c038323H
	DD	03e5d3bb9H
	DD	043d79572H
	DD	07e6dd07cH
	DD	06dfdf1eH
	DD	06c6cc4efH
	DD	07160a539H
	DD	073bfbe70H
	DD	083877605H
	DD	04523ecf1H
	DD	08defc240H
	DD	025fa5d9fH
	DD	0eb903dbfH
	DD	0e810c907H
	DD	047607fffH
	DD	0369fe44bH
	DD	08c1fc644H
	DD	0aececa90H
	DD	0beb1f9bfH
	DD	0eefbcaeaH
	DD	0e8cf1950H
	DD	051df07aeH
	DD	0920e8806H
	DD	0f0ad0548H
	DD	0e13c8d83H
	DD	0927010d5H
	DD	011107d9fH
	DD	07647db9H
	DD	0b2e3e4d4H
	DD	03d4f285eH
	DD	0b9afa820H
	DD	0fade82e0H
	DD	0a067268bH
	DD	08272792eH
	DD	0553fb2c0H
	DD	0489ae22bH
	DD	0d4ef9794H
	DD	0125e3fbcH
	DD	021fffceeH
	DD	0825b1bfdH
	DD	09255c5edH
	DD	01257a240H
	DD	04e1a8302H
	DD	0bae07fffH
	DD	0528246e7H
	DD	08e57140eH
	DD	03373f7bfH
	DD	08c9f8188H
	DD	0a6fc4ee8H
	DD	0c982b5a5H
	DD	0a8c01db7H
	DD	0579fc264H
	DD	067094f31H
	DD	0f2bd3f5fH
	DD	040fff7c1H
	DD	01fb78dfcH
	DD	08e6bd2c1H
	DD	0437be59bH
	DD	099b03dbfH
	DD	0b5dbc64bH
	DD	0638dc0e6H
	DD	055819d99H
	DD	0a197c81cH
	DD	04a012d6eH
	DD	0c5884a28H
	DD	0ccc36f71H
	DD	0b843c213H
	DD	06c0743f1H
	DD	08309893cH
	DD	0feddd5fH
	DD	02f7fe850H
	DD	0d7c07f7eH
	DD	02507fbfH
	DD	05afb9a04H
	DD	0a747d2d0H
	DD	01651192eH
	DD	0af70bf3eH
	DD	058c31380H
	DD	05f98302eH
	DD	0727cc3c4H
	DD	0a0fb402H
	DD	0f7fef82H
	DD	08c96fdadH
	DD	05d2c2aaeH
	DD	08ee99a49H
	DD	050da88b8H
	DD	08427f4a0H
	DD	01eac5790H
	DD	0796fb449H
	DD	08252dc15H
	DD	0efbd7d9bH
	DD	0a672597dH
	DD	0ada840d8H
	DD	045f54504H
	DD	0fa5d7403H
	DD	0e83ec305H
	DD	04f91751aH
	DD	0925669c2H
	DD	023efe941H
	DD	0a903f12eH
	DD	060270df2H
	DD	0276e4b6H
	DD	094fd6574H
	DD	0927985b2H
	DD	08276dbcbH
	DD	02778176H
	DD	0f8af918dH
	DD	04e48f79eH
	DD	08f616ddfH
	DD	0e29d840eH
	DD	0842f7d83H
	DD	0340ce5c8H
	DD	096bbb682H
	DD	093b4b148H
	DD	0ef303cabH
	DD	0984faf28H
	DD	0779faf9bH
	DD	092dc560dH
	DD	0224d1e20H
	DD	08437aa88H
	DD	07d29dc96H
	DD	02756d3dcH
	DD	08b907ceeH
	DD	0b51fd240H
	DD	0e7c07ce3H
	DD	0e566b4a1H
	DD	0c3e9615eH
	DD	03cf8209dH
	DD	06094d1e3H
	DD	0cd9ca341H
	DD	05c76460eH
	DD	0ea983bH
	DD	0d4d67881H
	DD	0fd47572cH
	DD	0f76cedd9H
	DD	0bda8229cH
	DD	0127dadaaH
	DD	0438a074eH
	DD	01f97c090H
	DD	081bdb8aH
	DD	093a07ebeH
	DD	0b938ca15H
	DD	097b03cffH
	DD	03dc2c0f8H
	DD	08d1ab2ecH
	DD	064380e51H
	DD	068cc7bfbH
	DD	0d90f2788H
	DD	012490181H
	DD	05de5ffd4H
	DD	0dd7ef86aH
	DD	076a2e214H
	DD	0b9a40368H
	DD	0925d958fH
	DD	04b39fffaH
	DD	0ba39aee9H
	DD	0a4ffd30bH
	DD	0faf7933bH
	DD	06d498623H
	DD	0193cbcfaH
	DD	027627545H
	DD	0825cf47aH
	DD	061bd8ba0H
	DD	0d11e42d1H
	DD	0cead04f4H
	DD	0127ea392H
	DD	010428db7H
	DD	08272a972H
	DD	09270c4a8H
	DD	0127de50bH
	DD	0285ba1c8H
	DD	03c62f44fH
	DD	035c0eaa5H
	DD	0e805d231H
	DD	0428929fbH
	DD	0b4fcdf82H
	DD	04fb66a53H
	DD	0e7dc15bH
	DD	01f081fabH
	DD	0108618aeH
	DD	0fcfd086dH
	DD	0f9ff2889H
	DD	0694bcc11H
	DD	0236a5caeH
	DD	012deca4dH
	DD	02c3f8cc5H
	DD	0d2d02dfeH
	DD	0f8ef5896H
	DD	0e4cf52daH
	DD	095155b67H
	DD	0494a488cH
	DD	0b9b6a80cH
	DD	05c8f82bcH
	DD	089d36b45H
	DD	03a609437H
	DD	0ec00c9a9H
	DD	044715253H
	DD	0a874b49H
	DD	0d773bc40H
	DD	07c34671cH
	DD	02717ef6H
	DD	04feb5536H
	DD	0a2d02fffH
	DD	0d2bf60c4H
	DD	0d43f03c0H
	DD	050b4ef6dH
	DD	07478cd1H
	DD	06e1888H
	DD	0a2e53f55H
	DD	0b9e6d4bcH
	DD	0a2048016H
	DD	097573833H
	DD	0d7207d67H
	DD	0de0f8f3dH
	DD	072f87b33H
	DD	0abcc4f33H
	DD	07688c55dH
	DD	07b00a6b0H
	DD	0947b0001H
	DD	0570075d2H
	DD	0f9bb88f8H
	DD	08942019eH
	DD	04264a5ffH
	DD	0856302e0H
	DD	072dbd92bH
	DD	0ee971b69H
	DD	06ea22fdeH
	DD	05f08ae2bH
	DD	0af7a616dH
	DD	0e5c98767H
	DD	0cf1febd2H
	DD	061efc8c2H
	DD	0f1ac2571H
	DD	0cc8239c2H
	DD	067214cb8H
	DD	0b1e583d1H
	DD	0b7dc3e62H
	DD	07f10bdceH
	DD	0f90a5c38H
	DD	0ff0443dH
	DD	0606e6dc6H
	DD	060543a49H
	DD	05727c148H
	DD	02be98a1dH
	DD	08ab41738H
	DD	020e1be24H
	DD	0af96da0fH
	DD	068458425H
	DD	099833be5H
	DD	0600d457dH
	DD	0282f9350H
	DD	08334b362H
	DD	0d91d1120H
	DD	02b6d8da0H
	DD	0642b1e31H
	DD	09c305a00H
	DD	052bce688H
	DD	01b03588aH
	DD	0f7baefd5H
	DD	04142ed9cH
	DD	0a4315c11H
	DD	083323ec5H
	DD	0dfef4636H
	DD	0a133c501H
	DD	0e9d3531cH
	DD	0ee353783H
	DD	09db30420H
	DD	01fb6e9deH
	DD	0a7be7befH
	DD	0d273a298H
	DD	04a4f7bdbH
	DD	064ad8c57H
	DD	085510443H
	DD	0fa020ed1H
	DD	07e287affH
	DD	0e60fb663H
	DD	095f35a1H
	DD	079ebf120H
	DD	0fd059d43H
	DD	06497b7b1H
	DD	0f3641f63H
	DD	0241e4adfH
	DD	028147f5fH
	DD	04fa2b8cdH
	DD	0c9430040H
	DD	0cc32220H
	DD	0fdd30b30H
	DD	0c0a5374fH
	DD	01d2d00d9H
	DD	024147b15H
	DD	0ee4d111aH
	DD	0fca5167H
	DD	071ff904cH
	DD	02d195ffeH
	DD	01a05645fH
	DD	0c13fefeH
	DD	081b08caH
	DD	05170121H
	DD	080530100H
	DD	0e83e5efeH
	DD	0ac9af4f8H
	DD	07fe72701H
	DD	0d2b8ee5fH
	DD	06df4261H
	DD	0bb9e9b8aH
	DD	07293ea25H
	DD	0ce84ffdfH
	DD	0f5718801H
	DD	03dd64b04H
	DD	0a26f263bH
	DD	07ed48400H
	DD	0547eebe6H
	DD	0446d4ca0H
	DD	06cf3d6f5H
	DD	02649abdfH
	DD	0aea0c7f5H
	DD	036338cc1H
	DD	0503f7e93H
	DD	0d3772061H
	DD	011b638e1H
	DD	072500e03H
	DD	0f80eb2bbH
	DD	0abe0502eH
	DD	0ec8d77deH
	DD	057971e81H
	DD	0e14f6746H
	DD	0c9335400H
	DD	06920318fH
	DD	081dbb99H
	DD	0ffc304a5H
	DD	04d351805H
	DD	07f3d5ce3H
	DD	0a6c866c6H
	DD	05d5bcca9H
	DD	0daec6feaH
	DD	09f926f91H
	DD	09f46222fH
	DD	03991467dH
	DD	0a5bf6d8eH
	DD	01143c44fH
	DD	043958302H
	DD	0d0214eebH
	DD	022083b8H
	DD	03fb6180cH
	DD	018f8931eH
	DD	0281658e6H
	DD	026486e3eH
	DD	08bd78a70H
	DD	07477e4c1H
	DD	0b506e07cH
	DD	0f32d0a25H
	DD	079098b02H
	DD	0e4eabb81H
	DD	028123b23H
	DD	069dead38H
	DD	01574ca16H
	DD	0df871b62H
	DD	0211c40b7H
	DD	0a51a9ef9H
	DD	014377bH
	DD	041e8ac8H
	DD	09114003H
	DD	0bd59e4d2H
	DD	0e3d156d5H
	DD	04fe876d5H
	DD	02f91a340H
	DD	0557be8deH
	DD	0eae4a7H
	DD	0ce5c2ecH
	DD	04db4bba6H
	DD	0e756bdffH
	DD	0dd3369acH
	DD	0ec17b035H
	DD	06572327H
	DD	099afc8b0H
	DD	056c8c391H
	DD	06b65811cH
	DD	05e146119H
	DD	06e85cb75H
	DD	0be07c002H
	DD	0c2325577H
	DD	0893ff4ecH
	DD	05bbfc92dH
	DD	0d0ec3b25H
	DD	0b7801ab7H
	DD	08d6d3b24H
	DD	020c763efH
	DD	0c366a5fcH
	DD	09c382880H
	DD	0ace3205H
	DD	0aac9548aH
	DD	0eca1d7c7H
	DD	041afa32H
	DD	01d16625aH
	DD	06701902cH
	DD	09b757a54H
	DD	031d477f7H
	DD	09126b031H
	DD	036cc6fdbH
	DD	0c70b8b46H
	DD	0d9e66a48H
	DD	056e55a79H
	DD	026a4cebH
	DD	052437effH
	DD	02f8f76b4H
	DD	0df980a5H
	DD	08674cde3H
	DD	0edda04ebH
	DD	017a9be04H
	DD	02c18f4dfH
	DD	0b7747f9dH
	DD	0ab2af7b4H
	DD	0efc34d20H
	DD	02e096b7cH
	DD	01741a254H
	DD	0e5b6a035H
	DD	0213d42f6H
	DD	02c1c7c26H
	DD	061c2f50fH
	DD	06552daf9H
	DD	0d2c231f8H
	DD	025130f69H
	DD	0d8167fa2H
	DD	0418f2c8H
	DD	01a96a6H
	DD	0d1526abH
	DD	063315c21H
	DD	05e0a72ecH
	DD	049bafefdH
	DD	0187908d9H
	DD	08d0dbd86H
	DD	0311170a7H
	DD	03e9b640cH
	DD	0cc3e10d7H
	DD	0d5cad3b6H
	DD	0caec388H
	DD	0f73001e1H
	DD	06c728affH
	DD	071eae2a1H
	DD	01f9af36eH
	DD	0cfcbd12fH
	DD	0c1de8417H
	DD	0ac07be6bH
	DD	0cb44a1d8H
	DD	08b9b0f56H
	DD	013988c3H
	DD	0b1c52fcaH
	DD	0b4be31cdH
	DD	0d8782806H
	DD	012a3a4e2H
	DD	06f7de532H
	DD	058fd7eb6H
	DD	0d01ee900H
	DD	024adffc2H
	DD	0f4990fc5H
	DD	09711aac5H
	DD	01d7b95H
	DD	082e5e7d2H
	DD	0109873f6H
	DD	0613096H
	DD	0c32d9521H
	DD	0ada121ffH
	DD	029908415H
	DD	07fbb977fH
	DD	0af9eb3dbH
	DD	029c9ed2aH
	DD	05ce2a465H
	DD	0a730f32cH
	DD	0d0aa3fe8H
	DD	08a5cc091H
	DD	0d49e2ce7H
	DD	0ce454a9H
	DD	0d60acd86H
	DD	015f1919H
	DD	077079103H
	DD	0dea03af6H
	DD	078a8565eH
	DD	0dee356dfH
	DD	021f05cbeH
	DD	08b75e387H
	DD	0b3c50651H
	DD	0b8a5c3efH
	DD	0d8eeb6d2H
	DD	0e523be77H
	DD	0c2154529H
	DD	02f69efdfH
	DD	0afe67afbH
	DD	0f470c4b2H
	DD	0f3e0eb5bH
	DD	0d6cc9876H
	DD	039e4460cH
	DD	01fda8538H
	DD	01987832fH
	DD	0ca007367H
	DD	0a99144f8H
	DD	0296b299eH
	DD	0492fc295H
	DD	09266beabH
	DD	0b5676e69H
	DD	09bd3dddaH
	DD	0df7e052fH
	DD	0db25701cH
	DD	01b5e51eeH
	DD	0f65324e6H
	DD	06afce36cH
	DD	0316cc04H
	DD	08644213eH
	DD	0b7dc59d0H
	DD	07965291fH
	DD	0ccd6fd43H
	DD	041823979H
	DD	0932bcdf6H
	DD	0b657c34dH
	DD	04edfd282H
	DD	07ae5290cH
	DD	03cb9536bH
	DD	0851e20feH
	DD	09833557eH
	DD	013ecf0b0H
	DD	0d3ffb372H
	DD	03f85c5c1H
	DD	0aef7ed2H
	DD	64247c83H
	DD	8b397558H
	DD	98249cH
	DD	7c8b0000H
	DD	478b3424H
	DD	483b81f4H
	DD	756b6361H
	DD	47b8123H
	DD	6f647265H
	DD	548b1a75H
	DD	0e86024H
	DD	5e000000H
	DD	0d0aee81H
	DD	8b900000H
	DD	0b1c933f8H
	DD	0fde2a560H
	DD	0b9e860c3H
	DD	61ffffffH

; mini-functions table
add_1 PROC
	mov eax, ecx
	add eax, edx
	ret
	db 3 dup (0CCh)
add_1 ENDP
xor_1:
	mov eax, ecx
	xor eax, edx
	ret
	db 3 dup (0CCh)
sub_1:
	mov eax, ecx
	sub eax, edx
	ret
	db 3 dup (0CCh)
add_2:
	mov eax, ecx
	add eax, edx
	ret
	db 3 dup (0CCh)
xor_2:
	mov eax, ecx
	xor eax, edx
	ret
	db 3 dup (0CCh)
sub_2:
	mov eax, ecx
	sub eax, edx
	ret
	db 3 dup (0CCh)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; f -- internal function for rounds ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

idx dw 0c7ebh
; args for f function
_y$ = 8
_x$ = 12
_kr$ = 16
_km$ = 20
_N$ = 24
f PROC
	push	ebp
	mov	ebp, esp
	mov	edx, DWORD PTR _x$[ebp]
	mov	ecx, DWORD PTR _km$[ebp]
	push	ebx
	push	esi
	mov	esi, DWORD PTR _N$[ebp]
	shl	esi, 3
	add	esi, OFFSET add_1
	call	esi
	mov	cl, BYTE PTR _kr$[ebp]
	mov	ebx, eax
	rol	ebx, cl
	add	esi, 8
	mov	eax, ebx
	shr	eax, 24
	mov	ecx, DWORD PTR s_box[eax*4]
	mov	eax, ebx
	shr	eax, 16
	movzx	eax, al
	mov	edx, DWORD PTR s_box[eax*4+1024]
	call	esi
	mov	ecx, ebx
	shr	ecx, 8
	movzx	ecx, cl
	mov	edx, DWORD PTR s_box[ecx*4+2048]
	add	esi, 8
	mov	ecx, eax
	call	esi
	movzx	ecx, bl
	mov	edx, DWORD PTR s_box[ecx*4+3072]
	add	esi, 8
	mov	ecx, eax
	call	esi
	mov	ecx, DWORD PTR _y$[ebp]
	xor	DWORD PTR [ecx], eax
	pop	esi
	pop	ebx
	pop	ebp
	ret	0
f ENDP

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; f_rnd, i_rnd, k_rnd - round functions ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; args for f_rnd
_x$ = 8
_n$ = 12
f_rnd PROC
	push	ebx
	push	esi
	mov	esi, DWORD PTR _n$[esp+4]
	push	edi
	mov	edi, DWORD PTR _x$[esp+8]
	push	0
	shl	esi, 2
	push	DWORD PTR l_key[esi+16]
	lea	ebx, DWORD PTR [edi+12]
	push	DWORD PTR l_key[esi]
	lea	eax, DWORD PTR [edi+8]
	push	DWORD PTR [ebx]
	push	eax
	call	f
	push	1
	push	DWORD PTR l_key[esi+20]
	lea	eax, DWORD PTR [edi+4]
	push	DWORD PTR l_key[esi+4]
	push	DWORD PTR [edi+8]
	push	eax
	call	f
	push	2
	push	DWORD PTR l_key[esi+24]
	push	DWORD PTR l_key[esi+8]
	push	DWORD PTR [edi+4]
	push	edi
	call	f
	push	0
	push	DWORD PTR l_key[esi+28]
	push	DWORD PTR l_key[esi+12]
	push	DWORD PTR [edi]
	push	ebx
	call	f
	add	esp, 80
	pop	edi
	pop	esi
	pop	ebx
	ret	0
f_rnd ENDP


_x$ = 8
tv208 = 12
_n$ = 12
i_rnd PROC
	push	ebp
	mov	ebp, esp
	push	ebx
	push	esi
	mov	esi, DWORD PTR _n$[ebp]
	push	edi
	mov	edi, DWORD PTR _x$[ebp]
	push	3
	shl	esi, 2
	push	DWORD PTR l_key[esi+28]
	lea	ebx, DWORD PTR [edi+12]
	push	DWORD PTR l_key[esi+12]
	push	DWORD PTR [edi]
	push	ebx
	call	f
	add esp, 20
	push	2
	push	DWORD PTR l_key[esi+24]
	lea	eax, DWORD PTR [edi+4]
	push	DWORD PTR l_key[esi+8]
	mov	DWORD PTR tv208[ebp], eax
	push	DWORD PTR [eax]
	push	edi
	call	f
	add esp, 20
	push	1
	push	DWORD PTR l_key[esi+20]
	add	edi, 8
	push	DWORD PTR l_key[esi+4]
	push	DWORD PTR [edi]
	push	DWORD PTR tv208[ebp]
	call	f
	add esp, 20
	push	0
	push	DWORD PTR l_key[esi+16]
	push	DWORD PTR l_key[esi]
	push	DWORD PTR [ebx]
	push	edi
	call	f
	add	esp, 20
	pop	edi
	pop	esi
	pop	ebx
	pop	ebp
	ret	0
i_rnd ENDP

tv196 = 8
_k$ = 8
_tr$ = 12
_tm$ = 16
k_rnd PROC
	push	ebp
	mov	ebp, esp
	push	ebx
	mov	ebx, DWORD PTR _tr$[ebp]
	push	esi
	mov	esi, DWORD PTR _k$[ebp]
	push	edi
	mov	edi, DWORD PTR _tm$[ebp]
	push	0
	push	DWORD PTR [edi]
	lea	eax, DWORD PTR [esi+28]
	push	DWORD PTR [ebx]
	lea	ecx, DWORD PTR [esi+24]
	push	DWORD PTR [eax]
	mov	DWORD PTR tv196[ebp], eax
	push	ecx
	call	f
	push	1
	push	DWORD PTR [edi+4]
	lea	eax, DWORD PTR [esi+20]
	push	DWORD PTR [ebx+4]
	push	DWORD PTR [esi+24]
	push	eax
	call	f
	push	2
	push	DWORD PTR [edi+8]
	lea	eax, DWORD PTR [esi+16]
	push	DWORD PTR [ebx+8]
	push	DWORD PTR [esi+20]
	push	eax
	call	f
	push	0
	push	DWORD PTR [edi+12]
	lea	eax, DWORD PTR [esi+12]
	push	DWORD PTR [ebx+12]
	push	DWORD PTR [esi+16]
	push	eax
	call	f
	add	esp, 80
	push	1
	push	DWORD PTR [edi+16]
	lea	eax, DWORD PTR [esi+8]
	push	DWORD PTR [ebx+16]
	push	DWORD PTR [esi+12]
	push	eax
	call	f
	push	2
	push	DWORD PTR [edi+20]
	lea	eax, DWORD PTR [esi+4]
	push	DWORD PTR [ebx+20]
	push	DWORD PTR [esi+8]
	push	eax
	call	f
	push	0
	push	DWORD PTR [edi+24]
	push	DWORD PTR [ebx+24]
	push	DWORD PTR [esi+4]
	push	esi
	call	f
	push	1
	push	DWORD PTR [edi+28]
	push	DWORD PTR [ebx+28]
	push	DWORD PTR [esi]
	push	DWORD PTR tv196[ebp]
	call	f
	add	esp, 80
	pop	edi
	pop	esi
	pop	ebx
	pop	ebp
	ret	0
k_rnd ENDP

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; set_key -- initialise the key schedule from the user supplied key ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; local vars for set_key
_tr$ = -96
_tm$ = -64
_lk$ = -32
; args for set_key
_in_key$ = 8
tv426 = 12
_key_len$ = 12
set_key PROC
	push	ebp
	mov	ebp, esp
	mov	eax, DWORD PTR _key_len$[ebp]
	sub	esp, 96
	push	ebx
	shr	eax, 5
	push	esi
	xor	edx, edx
	push	edi
	test	eax, eax
	jbe	SHORT $sk1
	mov	esi, DWORD PTR _in_key$[ebp]
	mov	ecx, eax
	lea	edi, DWORD PTR _lk$[ebp]
	rep movsd
	mov	edx, eax
	cmp	eax, 8
	jae	SHORT $sk2
$sk1:
	push	8
	pop	ecx
	sub	ecx, edx
	lea	edi, DWORD PTR _lk$[ebp+edx*4]
	xor	eax, eax
	rep stosd
$sk2:
	and	DWORD PTR tv426[ebp], 0
	push	19
	mov	esi, 1518500249
	pop	edi
	mov	ebx, 1859775393
$sk3:
	xor	eax, eax
$sk4:
	mov	DWORD PTR _tm$[ebp+eax], esi
	mov	DWORD PTR _tr$[ebp+eax], edi
	add	eax, 4
	add	esi, ebx
	add	edi, 17
	cmp	eax, 32
	jb	SHORT $sk4
	lea	eax, DWORD PTR _tm$[ebp]
	push	eax
	lea	eax, DWORD PTR _tr$[ebp]
	push	eax
	lea	eax, DWORD PTR _lk$[ebp]
	push	eax
	call	k_rnd
	add	esp, 12
	xor	eax, eax
$sk5:
	mov	DWORD PTR _tm$[ebp+eax], esi
	mov	DWORD PTR _tr$[ebp+eax], edi
	add	eax, 4
	add	esi, ebx
	add	edi, 17
	cmp	eax, 32
	jb	SHORT $sk5
	lea	eax, DWORD PTR _tm$[ebp]
	push	eax
	lea	eax, DWORD PTR _tr$[ebp]
	push	eax
	lea	eax, DWORD PTR _lk$[ebp]
	push	eax
	call	k_rnd
	mov	eax, DWORD PTR tv426[ebp]
	mov	ecx, DWORD PTR _lk$[ebp]
	mov	DWORD PTR l_key[eax], ecx
	mov	ecx, DWORD PTR _lk$[ebp+8]
	mov	DWORD PTR l_key[eax+4], ecx
	mov	ecx, DWORD PTR _lk$[ebp+16]
	mov	DWORD PTR l_key[eax+8], ecx
	mov	ecx, DWORD PTR _lk$[ebp+24]
	mov	DWORD PTR l_key[eax+12], ecx
	mov	ecx, DWORD PTR _lk$[ebp+28]
	mov	DWORD PTR l_key[eax+16], ecx
	mov	ecx, DWORD PTR _lk$[ebp+20]
	mov	DWORD PTR l_key[eax+20], ecx
	mov	ecx, DWORD PTR _lk$[ebp+12]
	mov	DWORD PTR l_key[eax+24], ecx
	mov	ecx, DWORD PTR _lk$[ebp+4]
	mov	DWORD PTR l_key[eax+28], ecx
	add	eax, 32
	add	esp, 12
	mov	DWORD PTR tv426[ebp], eax
	cmp	eax, 384
	jb	$sk3
	pop	edi
	pop	esi
	mov	eax, OFFSET l_key
	pop	ebx
	leave
	ret	0
set_key ENDP

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; encrypt -- encrypt block of open text ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

_blk$ = -16
_in_blk$ = 8
_out_blk$ = 12
encrypt PROC
	push	ebp
	mov	ebp, esp
	sub	esp, 16
	mov	eax, DWORD PTR _in_blk$[ebp]
	mov	ecx, DWORD PTR [eax]
	mov	DWORD PTR _blk$[ebp], ecx
	mov	ecx, DWORD PTR [eax+4]
	mov	DWORD PTR _blk$[ebp+4], ecx
	mov	ecx, DWORD PTR [eax+8]
	mov	eax, DWORD PTR [eax+12]
	mov	DWORD PTR _blk$[ebp+12], eax
	lea	eax, DWORD PTR _blk$[ebp]
	push	0
	push	eax
	mov	DWORD PTR _blk$[ebp+8], ecx
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	8
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	16
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	24
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	32
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	40
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	48
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	56
	push	eax
	call	i_rnd
	add	esp, 64
	lea	eax, DWORD PTR _blk$[ebp]
	push	64
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	72
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	80
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	88
	push	eax
	call	i_rnd
	mov	eax, DWORD PTR _out_blk$[ebp]
	mov	ecx, DWORD PTR _blk$[ebp]
	mov	DWORD PTR [eax], ecx
	mov	ecx, DWORD PTR _blk$[ebp+4]
	mov	DWORD PTR [eax+4], ecx
	mov	ecx, DWORD PTR _blk$[ebp+8]
	mov	DWORD PTR [eax+8], ecx
	mov	ecx, DWORD PTR _blk$[ebp+12]
	add	esp, 32
	mov	DWORD PTR [eax+12], ecx
	leave
	ret	0
encrypt ENDP


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; decrypt -- decrypt block of ciphercode ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; local var for decrypt
_blk$ = -16
; args for decrypt
_in_blk$ = 8
_out_blk$ = 12
decrypt PROC
	push	ebp
	mov	ebp, esp
	sub	esp, 16
	mov	eax, DWORD PTR _in_blk$[ebp]
	mov	ecx, DWORD PTR [eax]
	mov	DWORD PTR _blk$[ebp], ecx
	mov	ecx, DWORD PTR [eax+4]
	mov	DWORD PTR _blk$[ebp+4], ecx
	mov	ecx, DWORD PTR [eax+8]
	mov	eax, DWORD PTR [eax+12]
	mov	DWORD PTR _blk$[ebp+12], eax
	lea	eax, DWORD PTR _blk$[ebp]
	push	88
	push	eax
	mov	DWORD PTR _blk$[ebp+8], ecx
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	80
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	72
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	64
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	56
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	48
	push	eax
	call	f_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	40
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	32
	push	eax
	call	i_rnd
	add	esp, 64
	lea	eax, DWORD PTR _blk$[ebp]
	push	24
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	16
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	8
	push	eax
	call	i_rnd
	lea	eax, DWORD PTR _blk$[ebp]
	push	0
	push	eax
	call	i_rnd
	mov	eax, DWORD PTR _out_blk$[ebp]
	mov	ecx, DWORD PTR _blk$[ebp]
	mov	DWORD PTR [eax], ecx
	mov	ecx, DWORD PTR _blk$[ebp+4]
	mov	DWORD PTR [eax+4], ecx
	mov	ecx, DWORD PTR _blk$[ebp+8]
	mov	DWORD PTR [eax+8], ecx
	mov	ecx, DWORD PTR _blk$[ebp+12]
	add	esp, 32
	mov	DWORD PTR [eax+12], ecx
	leave
	ret	0
decrypt ENDP

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; test function for standalone version ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; local vars for main
_outb$ = -36
_data$ = -20
_key$ = -4
main	PROC
	push	ebp
	mov	ebp, esp
	sub	esp, 36
	lea	eax, DWORD PTR _key$[ebp]
	push	32
	push	eax
	mov	DWORD PTR _key$[ebp], 1768779620 ; hardcoded key for testing purposes
	call	set_key

	lea	eax, DWORD PTR _outb$[ebp]
	push	eax
	push	offset text_text
	call	encrypt

	lea	eax, DWORD PTR _outb$[ebp]
	push	eax
	push	offset text_text+16
	call	encrypt

	lea	eax, DWORD PTR _data$[ebp]
	push	eax
	lea	eax, DWORD PTR _outb$[ebp]
	push	eax
	call	decrypt
	xor	eax, eax
	leave
	ret	0
main	ENDP

_TEXT	ENDS
END
