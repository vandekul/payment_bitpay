# payment_bitpay
Gateway to Bitpay for Odoo v9.0
<html xmlns="http://www.w3.org/1999/html">
<body>

<section class="oe_container">
    <div class="oe_row oe_spaced">
        <h2 class="oe_slogan">Bitpay Gateway</h2>
        <h3 class="oe_slogan">This is the module to connect Odoo 9.0 and Bitpay</h3>
        <div class="oe_span6">
            <p class='oe_mt32'>
            This module allow you to create an easily way to accept cryptocurrencies.
            </p>
        </div>
    </div>
</section>

<section class="oe_container">
    <div class="oe_row oe_spaced">
        <h2 class="oe_slogan">Pre-Configure in your Server</h2>
        <div class="oe_span6">
            <p class='oe_mt32'>
            Before installing the module you will need to install this two libraries: <b>bitpay-python-py2</b> and <b>python-ecdsa</b>
            </p>
        </div>
    </div>
</section>

<section class="oe_container">
    <div class="oe_row oe_spaced">
        <h2 class="oe_slogan">Configure Payment Acquirer</h2>
        <div class="oe_span6">
            <p class='oe_mt32'>
                <ul>
                    <li>Install BitPay Module -> Website -> eCommerce -> Payment Acquirers -> BitPay</li>
                    <li>Put your wanted token. Best option is 'merchant'.</li>
                    <li>Put the location as test or live.</li>
                    <li>Put your account E-mail in Bitpay (optional).</li>
                    <li>Put and e-mail where you want to receive notifications (optional).</li>
                    <li>Put the Confirmation URL where Bitpay will return after payment.</li>
                    <li>Check if you want that Odoo send an email to your buyer after transaction is "Confirmed"</li>
                </ul>
            </p>
        </div>
    </div>
</section>

<section class="oe_container">
    <div class="oe_row oe_spaced">
        <h2 class="oe_slogan">Transaction Bitpay Details</h2>  
        <div class="oe_span6">
            <p class='oe_mt32'>
                <ul>
                    In transaction object, you will find more technical information about this method of payment:
                    <li>Transaction Id: cryptocurrency transaction hash for the executed payout.</li>
                    <li>Invoice Id: the id of the invoice for which you want to fetch an event token</li>
                    <li>Transaction Status: That indicates state of transaction</li>
                    <li>Buyer Mail Notification: Indicates if mail has been sent or if not (it will be in blank)</li>
                </ul>
            </p>
        </div>
    </div>
</section>
</body>
</html>
