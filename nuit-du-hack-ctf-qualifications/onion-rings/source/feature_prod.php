<?php include('db.php');
	$bdd = db_connect();
	$rep = $bdd->query('SELECT * FROM products WHERE feature = 1');
?>
	<div>		  
		  <h3 class="center">Feature Products </h3>
		  
		  <ul class="thumbnails">
<?php
	while ($donnees = $rep->fetch())
	{
		$descr_short = (strlen($donnees['description']) > 150) ? substr($donnees['description'],0,150).'...' : $$donnees['description'];
?>
	    <li class="span9">
		  <div class="thumbnail_feature">
			<?php echo("<a  href=\"product_details.php?id=".$donnees['id']."\"><img src=\"assets/products/".$donnees['pic_name']."\" /></a>\n<div class=\"caption\">");
			  echo("<h5>".$donnees['name']."</h5>");
			  echo("<p>\n".$descr_short."</p>");
			  echo("<div><a href=\"product_details.php?id=".$donnees['id']."\" >VIEW</a> <span class=\"pull-right\">".$donnees['price']."$</span></div>");?>
			</div>
		  </div>
		</li>
	



	<?php
		}

?>