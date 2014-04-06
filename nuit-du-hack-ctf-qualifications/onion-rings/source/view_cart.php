<?php session_start();
include 'header.php'; ?>
<div class="row">
<?php include 'sidebar.php'; ?>
    <div class="cart_container">
    <h2 class="center">Your Shopping Cart</h2>
    <?php
    $current_url = base64_encode($url="http://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
    if(isset($_SESSION['products']))
    {
        $total = 0;
        echo '<ul>';
        foreach ($_SESSION["products"] as $cart_itm)
        { ?>
        <div>
            <li class="cart_item">
                <?php echo '<h3>'.$cart_itm["name"].'</h3>';
                echo '<div class="p-price">Price :'.$cart_itm["price"].'</div>';
                echo '<div class="p-qty">Qty : '.$cart_itm["qty"].'</div>';
                echo '<a href="update_cart.php?removep='.$cart_itm["id"].'&return_url='.$current_url.'"> Delete </a>';
                $subtotal = ($cart_itm["price"]*$cart_itm["qty"]);
            $total = ($total + $subtotal); ?>
        </li>
    </div>
        <?php } ?>
        
        </ul>
    <?php 
    echo("<h3>Total: ".$total."</h3");
}
    else {
        echo 'Your Cart is empty';
    }
    ?>

    <div>
        <a class="btn btn-large pull-right" href="payment.php?">Checkout</a>
    </div>

    <script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
    <script src="assets/js/jquery.js"></script>
    <script src="assets/js/google-code-prettify/prettify.js"></script>
    <script src="assets/js/application.js"></script>
    <script src="assets/js/bootstrap-transition.js"></script>
    <script src="assets/js/bootstrap-modal.js"></script>
    <script src="assets/js/bootstrap-scrollspy.js"></script>
    <script src="assets/js/bootstrap-alert.js"></script>
    <script src="assets/js/bootstrap-dropdown.js"></script>
    <script src="assets/js/bootstrap-tab.js"></script>
    <script src="assets/js/bootstrap-tooltip.js"></script>
    <script src="assets/js/bootstrap-popover.js"></script>
    <script src="assets/js/bootstrap-button.js"></script>
    <script src="assets/js/bootstrap-collapse.js"></script>
    <script src="assets/js/bootstrap-carousel.js"></script>
    <script src="assets/js/bootstrap-typeahead.js"></script>
    <script src="assets/js/bootstrap-affix.js"></script>
    <script src="assets/js/jquery.lightbox-0.5.js"></script>
    <script src="assets/js/bootsshoptgl.js"></script>
     <script type="text/javascript">
    $(function() {
        $('#gallery a').lightBox();
    });
    </div>
</div>